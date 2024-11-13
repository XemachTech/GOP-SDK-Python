import os
from util.Constants import Constants


class FileItem:
    def __init__(
        self,
        file=None,
        file_path=None,
        file_name=None,
        content=None,
        stream=None,
        mime_type=None,
    ):
        if file:
            self.contract = LocalContract(file)
        elif file_path:
            self.contract = LocalContract(file_path)
        elif content is not None:
            self.contract = ByteArrayContract(file_name, content, mime_type)
        elif stream:
            self.contract = StreamContract(file_name, stream, mime_type)

    def is_valid(self):
        return self.contract.is_valid()

    def get_file_name(self):
        return self.contract.get_file_name()

    def get_mime_type(self):
        return self.contract.get_mime_type()

    def get_file_length(self):
        return self.contract.get_file_length()

    def write(self, output):
        self.contract.write(output)


class Contract:
    def is_valid(self):
        raise NotImplementedError

    def get_file_name(self):
        raise NotImplementedError

    def get_mime_type(self):
        raise NotImplementedError

    def get_file_length(self):
        raise NotImplementedError

    def write(self, output):
        raise NotImplementedError


class LocalContract(Contract):
    def __init__(self, file):
        if isinstance(file, str):
            self.file = open(file, "rb")
        else:
            self.file = file

    def is_valid(self):
        return self.file is not None and os.path.isfile(self.file.name)

    def get_file_name(self):
        return os.path.basename(self.file.name)

    def get_mime_type(self):
        return Constants.MIME_TYPE_DEFAULT

    def get_file_length(self):
        return os.path.getsize(self.file.name)

    def write(self, output):
        with self.file as input:
            buffer = input.read(Constants.READ_BUFFER_SIZE)
            while buffer:
                output.write(buffer)
                buffer = input.read(Constants.READ_BUFFER_SIZE)


class ByteArrayContract(Contract):
    def __init__(self, file_name, content, mime_type):
        self.file_name = file_name
        self.content = content
        self.mime_type = mime_type or Constants.MIME_TYPE_DEFAULT

    def is_valid(self):
        return self.content is not None and self.file_name is not None

    def get_file_name(self):
        return self.file_name

    def get_mime_type(self):
        return self.mime_type

    def get_file_length(self):
        return len(self.content)

    def write(self, output):
        output.write(self.content)


class StreamContract(Contract):
    def __init__(self, file_name, stream, mime_type):
        self.file_name = file_name
        self.stream = stream
        self.mime_type = mime_type or Constants.MIME_TYPE_DEFAULT

    def is_valid(self):
        return self.stream is not None and self.file_name is not None

    def get_file_name(self):
        return self.file_name

    def get_mime_type(self):
        return self.mime_type

    def get_file_length(self):
        return 0

    def write(self, output):
        buffer = self.stream.read(Constants.READ_BUFFER_SIZE)
        while buffer:
            output.write(buffer)
            buffer = self.stream.read(Constants.READ_BUFFER_SIZE)
        self.stream.close()
