from utils import check_str_is_binary, message_generator

import more_itertools

from processors import BaseStegoProcessor, get_io_class


class StegoPipeline:
    def __init__(self, img, steps):
        # adds pipeline steps, with error checking
        self._pipeline = []
        self.pipeline = steps

        # the IO object (containing the image)
        self.io = get_io_class(img)

    ##############
    # PROPERTIES #
    ##############
    @property
    def pipeline(self):
        return self._pipeline

    @pipeline.setter
    def pipeline(self, steps):
        # checks over each step
        for step in steps:
            # parses the step
            name, processor = step

            # checks that the name is a string
            if not isinstance(name, str) or len(name) <= 0:
                raise ValueError(f"All processor names must be strings with a length")

            # checks that the step is an instance of a stego processor
            if not isinstance(processor, BaseStegoProcessor):
                raise ValueError(f"All processors must be children classes of BaseStegoProcessor: {processor}")

        self._pipeline = steps

    ###################
    # PRIVATE METHODS #
    ###################
    def _run_pipeline(self, steps, method, data, msg=None):
        # iterates over each step
        for name, processor in steps:
            # tries to process the data
            # DEBUG
            # try:
            # we don't know the function beforehand (hide versus extract),
            # so uses a dynamic call
            try:
                data = getattr(processor, method)(data=data, msg=msg)
            except Exception as e:
                raise Exception(f"Error executing processing step {name}: {processor}:\n{e}")

        return data

    ##################
    # PUBLIC METHODS #
    ##################
    def hide(self, msg, file_path):
        # reads the data
        data = self.io.read()
        msg_generator = more_itertools.peekable(message_generator(msg))

        # runs the pipeline to transform the data
        data = self._run_pipeline(steps=self.pipeline, method="hide", data=data, msg=msg_generator)

        # converts the data into tuples
        data = [tuple(colors) for colors in data]

        # now writes the image
        self.io.write(data, file_path)

    def extract(self, file_path):
        # reads the data
        data = self.io.read()

        # runs the pipeline
        data = self._run_pipeline(steps=self.pipeline[::-1], method="extract", data=data)

        return data

    ##################
    # DUNDER METHODS #
    ##################
    # def __str__(self):
    #     return f"StegoPipeline. Steps={self.pipeline}"

    def __repr__(self):
        return f"StegoPipeline(\n\t\tsteps={self.pipeline})"
