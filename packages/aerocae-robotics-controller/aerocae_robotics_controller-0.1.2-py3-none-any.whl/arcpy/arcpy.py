import socket
import struct
import sys
from typing import NamedTuple

class Output(NamedTuple):
    outputs: dict

    def get_output_of(self, obj: int) -> tuple:
        if obj in self.outputs:
            return self.outputs[obj]
        
        return None
    

class SimulationResult(NamedTuple):
    failed: int
    outputs: dict

    def is_failed(self) -> bool:
        return self.failed != 0
    
    def get_output_of(self, obj: int) -> tuple:
        if obj in self.outputs:
            return self.outputs[obj]
        
        return None

buffer_size = 4096
uint_max = 4294967295

def uint_to_bytes(val : int) -> bytes:
    return int.to_bytes(val, 4, byteorder=sys.byteorder, signed=False)

def bytes_to_uint(data : bytes, offset : int) -> int:
    return int.from_bytes(data[offset:offset+4], byteorder=sys.byteorder, signed=False)

def double_to_bytes(val: float) -> bytes:
    return struct.pack('d', val)

def bytes_to_double(data: bytes, offset: int) -> float:
    return struct.unpack('d', data[offset:offset+8])[0]

def string_to_bytes(string: str) -> bytes:
    return string.encode("utf-8")

class MessagingClient:
    def __init__(self, host : str, port : int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def request(self, data : bytes) -> bytes:
        self.socket.send(data)
        return self.socket.recv(buffer_size)
    
    def close(self):
        self.socket.close()

class Controller:
    def __init__(self, host : str, port : int = 25556):
        self.messaging = MessagingClient(host, port)

    # Parameters: none
    # Returns: time step
    def get_time_step(self) -> float:
        reply = self.messaging.request(uint_to_bytes(0))
        return bytes_to_double(reply, 0)

    # Parameters: actuator name
    # Returns: None or (actuator index, actuator dof)
    def get_object_by_path(self, path : str, relative_to_object : int=None) -> int:
        request = uint_to_bytes(1)
        if relative_to_object is None:
            request += uint_to_bytes(uint_max)
        else:
            request += uint_to_bytes(relative_to_object)
        array = string_to_bytes(path)
        request += uint_to_bytes(len(array))
        request += array
        reply = self.messaging.request(request)
        obj = bytes_to_uint(reply, 0)
        if obj == uint_max:
            return None
        else:
            return obj
        
    # Parameters: list of object to retrieve output
    # Returns: Output
    def get_output(self, output_objs: list) -> Output:
        request = uint_to_bytes(2)
        request += uint_to_bytes(len(output_objs))
        for obj in output_objs:
            request += uint_to_bytes(obj)

        reply = self.messaging.request(request)
        count = bytes_to_uint(reply, 0)
        outputs = {}
        start = 4
        for i in range(count):
            obj = bytes_to_uint(reply, start)
            start += 4
            dof = bytes_to_uint(reply, start)
            start += 4
            output = []
            for j in range(dof):
                output.append(bytes_to_double(reply, start))
                start += 8
            outputs[obj] = tuple(output)
        
        return Output(outputs)
        
    # Parameters: none
    # Returns: (success, current state), where state = 0 for not running, 1 for running.
    def start(self) -> tuple[bool, int]:
        request = uint_to_bytes(3)
        request += b'\x00'
        reply = self.messaging.request(request)
        success = reply[0:1] == b'\x00'
        state = int.from_bytes(reply[1:2], byteorder=sys.byteorder, signed=False)
        return success, state
    
    # Parameters: none
    # Returns: (success, current state), where state = 0 for not running, 1 for running.
    def reset(self) -> tuple[bool, int]:
        request = uint_to_bytes(3)
        request += b'\x01'
        reply = self.messaging.request(request)
        success = reply[0:1] == b'\x00'
        state = int.from_bytes(reply[1:2], byteorder=sys.byteorder, signed=False)
        return success, state
    
    # Parameters: none
    # Returns: (success, current state), where state = 0 for not running, 1 for running.
    def clear(self) -> tuple[bool, int]:
        request = uint_to_bytes(3)
        request += b'\x02'
        reply = self.messaging.request(request)
        success = reply[0:1] == b'\x00'
        state = int.from_bytes(reply[1:2], byteorder=sys.byteorder, signed=False)
        return success, state
    
    # Parameters: steps to simulate, inputs, output_objs
    # (inputs: obj (int) -> input (tuple of float))
    # (output_objs: list of obj (int))
    # Returns: (status code, sensor outputs), where status code = 0 for success, 1 for inpur error, 2 for simulation error. 
    # (sensor outputs: index (int) -> output (tuple of float))
    def simulate(self, steps : int, inputs : dict, output_objs : list) -> SimulationResult:
        request = uint_to_bytes(4)
        request += uint_to_bytes(steps)
        request += uint_to_bytes(len(inputs))
        for obj in inputs:
            request += uint_to_bytes(obj)
            input = inputs[obj]
            request += uint_to_bytes(len(input))
            for val in input:
                request += struct.pack('d', val)
        request += uint_to_bytes(len(output_objs))
        for obj in output_objs:
            request += uint_to_bytes(obj)

        reply = self.messaging.request(request)
        failed = int.from_bytes(reply[0:1], byteorder=sys.byteorder, signed=False)
        if failed != 0:
            return SimulationResult(failed, dict())
        
        output_count = bytes_to_uint(reply, 1)
        start = 5
        outputs = {}
        for i in range(output_count):
            obj = bytes_to_uint(reply, start)
            start += 4
            dof = bytes_to_uint(reply, start)
            start += 4
            output = []
            for j in range(dof):
                output.append(bytes_to_double(reply, start))
                start += 8
            outputs[obj] = tuple(output)
        
        return SimulationResult(0, outputs)
        
    # Parameters: sequential number
    # Returns: success or not
    def export(self, seq_num : int) -> bool:
        request = uint_to_bytes(5)
        request += uint_to_bytes(seq_num)
        reply = self.messaging.request(request)
        return reply[0:1] == b'\x00'
    
    # parameters: object to clone, position, rotation, name
    # (position: a tuple of 3 float, in x, y, z)
    # (rotation: a tuple of 4 float, in quaternion w, x, y, z)
    # Returns: None if failed, otherwise the cloned object
    def clone_object(self, source_obj : int, position: tuple, rotation: tuple, name: str) -> int:
        request = uint_to_bytes(6)
        request += uint_to_bytes(source_obj)
        for i in range(3):
            request += double_to_bytes(position[i])
        for i in range(4):
            request += double_to_bytes(rotation[i])
        array = string_to_bytes(name)
        request += uint_to_bytes(len(array))
        request += array

        reply = self.messaging.request(request)
        failed = int.from_bytes(reply[0:1], byteorder=sys.byteorder, signed=False)
        if failed != 0:
            return None
        return bytes_to_uint(reply, 1)

    def close(self):
        self.messaging.close()