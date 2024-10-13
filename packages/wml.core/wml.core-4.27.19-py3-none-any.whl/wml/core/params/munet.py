import yaml


class MunetModelParams(yaml.YAMLObject):
    yaml_tag = "!MunetModelParams"

    """Parameters for creating a MuNetV6 or a MuNetV71 inference model.

    For backward compatibility reasons, we are yet able to rename the class to something more
    modern.

    Parameters
    ----------
    model_arch : {'munetv6', 'munetv71'}
        model arch to be created. Now we accept both V6 and V7.1
    backbone : {'mobilenetv2', 'mobilenetv2_truncated'}
        backbone to be used for feature extraction. 'mobilenetv2_truncated' is 'mobilenetv2' but we
        use two outputs. One is a lightweight 'block_6_expand_relu' tensor and the other is the
        output of mobilenetv2. The former is used as input for change detection, the latter is used
        as input for recognition.
    input_images_name : str
        name of the input image tensor
    input_ints_name : str
        name of the tensor containing all the input integers
    mask_head_name : str
        name of the tensor containing the (upsampled) change mask
    label_head_name : str
        name of the layer containing the label head
    mobilenetv2_alpha: float
        controls the width of the MobileNetV2 network. This is known as the
        width multiplier in the MobileNetV2 paper.

        - If `alpha` < 1.0, proportionally decreases the number of filters in each layer.
        - If `alpha` > 1.0, proportionally increases the number of filters in each layer.
        - If `alpha` = 1, default number of filters from the paper are used at each layer.

        Used only for mobilenetv2 backbones
    dropout : float
        dropout coefficient
    weight_decay : float
        weight decay coefficient for regularizers
    """

    def __init__(
        self,
        model_arch="munetv71",
        backbone="mobilenetv2",
        input_images_name="input_images",
        input_attrs_name="input_attrs",
        mask_head_name="output_mask",
        label_head_name="output_labels",
        mobilenetv2_alpha=1.0,
        dropout=0.2,
        weight_decay=0.00004,
    ):
        self.model_arch = model_arch
        self.backbone = backbone
        self.input_images_name = input_images_name
        self.input_attrs_name = input_attrs_name
        self.mask_head_name = mask_head_name
        self.label_head_name = label_head_name
        self.mobilenetv2_alpha = mobilenetv2_alpha
        self.dropout = dropout
        self.weight_decay = weight_decay


class MuNetV6InferenceModelParams(MunetModelParams):
    yaml_tag = "!MuNetV6InferenceModelParams"
