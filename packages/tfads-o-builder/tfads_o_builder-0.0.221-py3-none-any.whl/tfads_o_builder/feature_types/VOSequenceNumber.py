from tfads_o_builder.feature_types._Base import _Base


class VOSequenceNumber(_Base):
    def __init__(self):
        super().__init__()
        self.field_name = "VO Sequence Number"
