# Copyright 2018 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

import numpy as np
import os
import sys
import tarfile
from PIL import Image

png = '.png'
jpg = '.jpg'
jpeg = '.jpeg'
onnx_file = '.onnx'
tflite_file = '.tflite'
h5_file = '.h5'
tfhub_ext = 'https://tfhub.dev/'
convert_message = "Converted from "
signed = 'signed'
unsigned = 'unsigned'


def saved_model_exists(filename):
    """
    saved_model_exists(filename)

    Determines whether a filepath is a valid Saved Model file or directory.

    Parameters
    ----------
    filename : string
        The filepath to the Saved Model file/directory to be tested for validity.

    Returns
    -------
    valid : bool
        The validity of whether the file/directory is a Saved Model.
    """
    return os.path.isfile(filename + '/saved_model.pb') or \
           os.path.isfile(filename + '/saved_model.pbtxt') or \
           filename.endswith('saved_model.pb') or \
           filename.endswith('saved_model.pbtxt')


def convert_to_onnx(infile, outfile, input_names, output_names, samples, num_samples, default_shape,
                    quant_channel_bool, quantize=False, onnx_opset=11, quant_norm='unsigned', tflite_conv='mlir'):
    """
    convert_to_onnx(infile, outfile, input_names, output_names, samples, 
                    default_shape, quant_channel_bool, quantize=False, 
                    onnx_opset=11, quant_norm='unsigned', tflite_conv='mlir')

​	 Converts the provided model to ONNX


    Parameters
    ----------
    infile : str
        Specifies the path to a specific file or a TFHub URL of a given model 
        that is to be converted to ONNX.
    outfile : str
        The filepath of the output ONNX model.
    input_names : list
        This field is a list that contains strings that represent which layers 
        are expected to be the input layers within the ONNX model. They must 
        exist within the input model, but it is not necessary that they are 
        the inputs within that model, this allows for subgraphing capabilities.
    output_names : list
        This field is a list that contains strings that represent which layers 
        are expected to be the output layers within the ONNX model. They must 
        exist within the input model, but it is not necessary that they are the 
        outputs within that model, this allows for subgraphing capabilities.
    samples : str
        The location of dataset samples to be used for quantization. This can be 
        a filepath to a folder containing images or a URL to a datastore containing
        images.
    num_samples : int
        The number of samples to use from the provided dataset for quantization.
    default_shape : list
        The shape for the input layer of the model.
    quant_channel_bool : {True, False}
        This toggle will determine whether a quantized ONNX model uses per-tensor 
        or per-channel. If the value is True, then a quantized ONNX model will use 
        per-channel. If the value is False, the quantized ONNX model will use per-tensor.
    quantize : {True, False}, optional
        If true, the model will be converted to a quantized ONNX model, if False the 
        model will remain in it's original datatype representation.
    onnx_opset : int, optional
        This integer determines which opset will be used in conversion to ONNX, higher 
        opsets will provide increased availability of operators, but this may limit 
        functionality on some devices which do not have inference available for those 
        operations. View https://github.com/onnx/onnx/blob/master/docs/Operators.md 
        to see the list of when operations were introduced.
    quant_norm : {'unsigned', 'signed', 'imagenet'}, optional
        This field will determine the normalization used for images that will be used 
        for quantization. 'unsigned' will perform x / 255, 'signed' will perform 
        (x / 127.5) - 1. The 'imagenet' normalization performs channel specific 
        normalization.
    tflite_conv : {'mlir', 'toco'}, optional
        This field signifies which TFLite Converter shall be used for the intermediate 
        step of converting to TFLite when necessary, between the MLIR and TOCO converters.
    """
    import tensorflow as tf
    import tf2onnx
    experimental_new_conv = True
    if tflite_conv == 'toco':
        experimental_new_conv = False
    if (not input_names or not output_names) and not infile.endswith(tflite_file) \
            and not infile.endswith(h5_file) and not infile.startswith(tfhub_ext) \
            and not infile.endswith(onnx_file):
        raise ValueError("ERROR: Please provide input and output names")

    if not infile.endswith(tflite_file) and not infile.endswith(h5_file) \
            and not infile.startswith(tfhub_ext) and not infile.endswith(onnx_file):
        for i in range(len(input_names)):
            input_names[i] = input_names[i] + ':0'
        for i in range(len(output_names)):
            output_names[i] = output_names[i] + ':0'

    shape_override = {}
    if input_names is not None:
        for name in input_names:
            shape_override[name] = default_shape
    orig_filename = infile
    if type(infile) == str and \
            os.path.exists(infile) and \
            os.path.isfile(infile) and \
            tarfile.is_tarfile(infile):
        with tarfile.open(infile) as tar:
            infile = infile.replace(".tar.gz", "")
            infile = infile.replace(".tar.bz2", "")
            infile = infile.replace(".tar.xz", "")
            infile = infile.replace(".tgz", "")
            infile = infile.replace(".tar", "")
            print('EXTRACTING TAR FILE TO -> %s' % infile)
            tar.extractall(infile)
        if not os.path.exists(infile + '/saved_model.pb'):
            infile = infile + '/' + infile + '/saved_model'
        if not os.path.exists(infile + '/saved_model.pb'):
            raise ValueError("Unable to located 'saved_model.pb' file " \
                             "within the provided tarfile. Please manually unzip " \
                             "and convert using the directory that contains 'saved_model.pb'")
    if saved_model_exists(infile):
        import tempfile
        if not os.path.isdir(infile):
            infile = os.path.dirname(infile)
        loaded = tf.saved_model.load(infile)
        if not (list(loaded.signatures.keys())):
            print("WARNING, signature key not found. \n"
                  "Default shape is set to " + str(default_shape) + "\n"
                                                                    "Change default shape using --default_shape")
            with tempfile.TemporaryDirectory() as temp:
                module_with_signature_path = temp
                if not os.path.exists(module_with_signature_path):
                    os.mkdir(module_with_signature_path)
                call = loaded.__call__.get_concrete_function(tf.TensorSpec(default_shape, tf.float32))
                tf.saved_model.save(loaded, module_with_signature_path, signatures=call)
                graph_def, inputs, outputs = tf2onnx.tf_loader.from_saved_model(module_with_signature_path,
                                                                                input_names, output_names)
        else:
            graph_def, inputs, outputs = tf2onnx.tf_loader.from_saved_model(infile, input_names, output_names)
        with tf.Graph().as_default() as tf_graph:
            tf.import_graph_def(graph_def, name='')
            with tf2onnx.tf_loader.tf_session(graph=tf_graph):
                g = tf2onnx.tfonnx.process_tf_graph(tf_graph, input_names=inputs, shape_override=shape_override,
                                                    output_names=outputs, opset=onnx_opset)
        onnx_graph = tf2onnx.optimizer.optimize_graph(g)
        model_proto = onnx_graph.make_model(convert_message + "%s" % infile)
    elif infile.endswith('.pb'):
        # Trim pb first to possibly remove unsupported ops before onnx conversion
        import tempfile
        # Handle Tensorflow 2.0
        if len(input_names) > 1:
            raise ValueError("Unsupported pb trim - more than one input layer")
        if float(tf.__version__[:2]) >= 2.0:
            import tensorflow.compat.v1 as tf
        with open(infile, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

        new_graph_def = tf.GraphDef()
        input_names_orig = []
        output_names_orig = []
        for i in range(len(input_names)):
            input_names_orig.append(input_names[i].replace(':0', ''))
        for i in range(len(output_names)):
            output_names_orig.append(output_names[i].replace(':0', ''))
        pb_inputs = {}
        pb_inputs[input_names_orig[0]] = default_shape

        for tfnode in graph_def.node:
            if tfnode.name in pb_inputs.keys():
                node = tf.NodeDef(name=tfnode.name, op='Placeholder')
                node.attr['dtype'].type = 1
                for size in pb_inputs[tfnode.name]:
                    node.attr['shape'].shape.dim.add().size = size
                new_graph_def.node.extend([node])
            else:
                new_graph_def.node.extend([tfnode])

        out_graph_def = tf.GraphDef()
        with tf.Session() as sess:
            out_graph_def = tf.graph_util.convert_variables_to_constants(sess, new_graph_def, output_names_orig)
        # Secure tempfile
        pb_fd, pb_filename = tempfile.mkstemp()
        os.write(pb_fd, out_graph_def.SerializeToString())
        os.close(pb_fd)
        # Resume ONNX conversion using intermediate trimmed.pb - removed later
        import tensorflow as tf
        try:
            graph_def, inputs, outputs = tf2onnx.tf_loader.from_graphdef(pb_filename, input_names, output_names)
            with tf.Graph().as_default() as tf_graph:
                tf.import_graph_def(graph_def, name='')
                with tf2onnx.tf_loader.tf_session(graph=tf_graph):
                    g = tf2onnx.tfonnx.process_tf_graph(tf_graph, input_names=inputs, shape_override=shape_override,
                                                        output_names=outputs, opset=onnx_opset)
            onnx_graph = tf2onnx.optimizer.optimize_graph(g)
            model_proto = onnx_graph.make_model(convert_message + "%s" % infile)
        except Exception:
            os.remove(pb_filename)
            raise ValueError("Unsupported pb file or operation in tf2onnx...")
        os.remove(pb_filename)
    elif infile.endswith(tflite_file):
        try:
            g = tf2onnx.tfonnx.process_tf_graph(None, input_names, output_names, opset=onnx_opset, tflite_path=infile)
            onnx_graph = tf2onnx.optimizer.optimize_graph(g)
            model_proto = onnx_graph.make_model(convert_message + "%s" % infile)
        except Exception as e:
            if 'Opset 13' in str(e):
                raise ValueError(" Opset 13 Conversion Issue")
            else:
                raise ValueError("Third Party Conversion Issue")

    elif infile.endswith(onnx_file):
        if not quantize:
            from onnx.utils import extract_model
            import onnx
            default_input_names = []
            default_output_names = []
            if isinstance(infile, str):
                with open(infile, 'rb') as f:
                    input_model = f.read()

            onnx_model = onnx.ModelProto()
            onnx_model.ParseFromString(input_model)
            onnx_graph = onnx_model.graph

            for i in range(len(onnx_graph.input)):
                onnx_input = onnx_graph.input[i]
                name = onnx_input.name
                default_input_names.append(name)

            for i in range(len(onnx_graph.output)):
                onnx_output = onnx_graph.output[i]
                name = onnx_output.name
                default_output_names.append(name)

            if input_names is None or len(input_names) == 0:
                input_names = default_input_names
            
            if output_names is None or len(output_names) == 0:
                output_names = default_output_names

            try:
                extract_model(infile, outfile, input_names, output_names)
            except Exception as e:
                print(e)
            print("Generated trimmed ONNX: %s" % outfile)
            return

    elif infile.endswith(h5_file) or infile.startswith(tfhub_ext):
        import tensorflow_hub as hub
        if infile.startswith(tfhub_ext):
            keras_model = tf.keras.Sequential(
                [tf.keras.layers.InputLayer(input_shape=default_shape[1:]),
                 hub.KerasLayer(infile)])
        else:
            keras_model = tf.keras.models.load_model(infile, compile=False, 
                                                     custom_objects={'KerasLayer': hub.KerasLayer})
        converter = tf.lite.TFLiteConverter.from_keras_model(keras_model, )
        try:
            converter.experimental_new_converter = experimental_new_conv
            tflite_model = converter.convert()
        except Exception as e:
            if quantize:
                converter.experimental_new_quantizer = False
                tflite_model = converter.convert()
            else:
                raise e
        with open(outfile, "wb") as f:
            f.write(tflite_model)

        g = tf2onnx.tfonnx.process_tf_graph(None, input_names, output_names, opset=onnx_opset, tflite_path=outfile)
        onnx_graph = tf2onnx.optimizer.optimize_graph(g)
        model_proto = onnx_graph.make_model(convert_message + "%s" % infile)
    else:
        raise ValueError("ERROR: Incorrect Input File Format")

    if quantize:
        if infile.endswith(onnx_file):
            quantize_onnx_fp32models(infile, outfile, input_names, quant_norm, samples, 
                                     num_samples, default_shape, quant_channel_bool)
            return
        else:
            with open(outfile, "wb") as f:
                f.write(model_proto.SerializeToString())
            quantize_onnx_fp32models(outfile, outfile, input_names, quant_norm, samples,
                                     num_samples, default_shape, quant_channel_bool)
            return
    with open(outfile, "wb") as f:
        f.write(model_proto.SerializeToString())


def quantize_onnx_fp32models(infile, outfile, input_names, quant_norm, samples, num_samples,
                             default_shape, quant_channel_bool):
    """
    
    """
    import onnx
    import numpy as np
    import onnxruntime
    from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantFormat, quantize_dynamic

    class MulitInputDataReader(CalibrationDataReader):
        def __init__(self, samples_folders, norms, model):
            self.enum_data = []
            self.iter_data = None
            session = onnxruntime.InferenceSession(model)
            self.input_names = []
            self.input_shapes = []
            self.norms = norms.split(',')
            for sess_in in session.get_inputs():
                self.input_names.append(sess_in.name)
                self.input_shapes.append(sess_in.shape)
            num_inputs = len(input_names)
            samples_dict = {}                        
            
            for i in range(len(samples_folders)):
                for root, _, files in os.walk(samples_folders[i]):
                    for filename in files:
                        if not filename.lower().endswith(png) and \
                                not filename.lower().endswith(jpg) and \
                                not filename.lower().endswith(jpeg) and \
                                not filename.lower().endswith('.npy'):
                            continue
                        image_filepath = root + '/' + filename
                        base_name = filename[:filename.find('.')]
                        if base_name not in samples_dict:
                            samples_dict[base_name] = {}
                        samples_dict[base_name][i] = image_filepath
                        
            remove_keys = []
            for key, val in samples_dict.items():
                if len(val) != num_inputs:
                    remove_keys.append(key)
            for key in remove_keys:
                del samples_dict[key]

            if len(samples_dict) == 0:
                raise ValueError("Cannot find any usable images for quantization between the provided folders. " \
                                 "Please ensure all samples between folders use the same base filename for matching")
            
            for key, val in samples_dict.items():
                for i in range(num_inputs):
                    filename = val[i]
                    if filename.endswith('.npy'):
                        base_array = np.load(filename).astype(np.float32)
                    else:
                        image = Image.open(filename).convert('RGB')
                        if self.input_shapes[i][1] == 3:
                            image = image.resize((self.input_shapes[i][3], self.input_shapes[i][2]), Image.ANTIALIAS)
                            base_array = np.asarray(image).astype(np.float32)
                            base_array = np.transpose(base_array, [2,0,1])
                        else:
                            image = image.resize((self.input_shapes[i][2], self.input_shapes[i][1]), Image.ANTIALIAS)
                            base_array = np.asarray(image).astype(np.float32)
                        base_array = np.expand_dims(base_array, 0)
                    base_array = self.preprocess_array(base_array, i)

                    val[i] = base_array

            sample_count = 0
            for key, val in samples_dict.items():
                data_dict = {}
                for index, array in val.items():
                    data_dict[self.input_names[index]] = array
                self.enum_data.append(data_dict)
                sample_count += 1
                if sample_count >= num_samples:
                    break

        def preprocess_array(self, array, input_num):
            norm = self.norms[input_num]
            input_shape = self.input_shapes[i]
            if norm == 'radar':
                array = array[:, :input_shape[2], :, :, :]
                array = np.transpose(array, [0,2,4,1,3])
                array = array.reshape(input_shape)
                cutout = 50
                array[array <= -cutout] = -cutout
                array[array >= cutout] = cutout
                array = (array + cutout) / (2 * cutout)
            elif norm == 'unsigned':
                array = array / 255.0
            elif norm == 'signed':
                array = (array / 127.5) - 1
            elif norm == 'imagenet':
                mean = np.array([0.079, 0.05, 0]) + 0.406
                std = np.array([0.005, 0, 0.001]) + 0.224
                if array.shape[1] == 3:
                    for channel in range(array.shape[0]):
                        array[:, channel, :, :] = (array[:, channel, :, :] / 255 - mean[channel]) / std[channel]
                else:
                    for channel in range(array.shape[2]):
                        array[:, :, :, channel] = (array[:, :, :, channel] / 255 - mean[channel]) / std[channel]
            return array

        def get_next(self):
            if self.iter_data is None:
                self.iter_data = iter(self.enum_data)
            return next(self.iter_data, None)


    if input_names is None or len(input_names) == 0:
        default_input_names = []
        default_input_shapes = []
        if type(infile) == str:
            with open(infile, 'rb') as f:
                input_model = f.read()

        onnx_model = onnx.ModelProto()
        onnx_model.ParseFromString(input_model)
        onnx_graph = onnx_model.graph

        for i in range(len(onnx_graph.input)):
            onnx_input = onnx_graph.input[i]
            name = onnx_input.name
            default_input_names.append(name)
            onnx_dims = onnx_input.type.tensor_type.shape.dim
            in_shape = []
            for j in range(len(onnx_dims)):
                if onnx_dims[j].dim_param != '':
                    in_shape.append(-1)
                else:
                    in_shape.append(onnx_dims[j].dim_value)
            if len(in_shape) == len(default_shape) and -1 in in_shape[1:]:
                print(f"The ONNX model does not have a definitive input shape for "
                    "input {name}, using default shape of [" + 
                    ','.join(str(def_dim) for def_dim in default_shape) + "].")
                in_shape = default_shape
            if in_shape[0] == -1:
                in_shape[0] = 1
            default_input_shapes.append(in_shape)

        input_names = default_input_names

    data_reader = MulitInputDataReader(samples, quant_norm, infile)

    quantize_static(infile,
                    outfile,
                    data_reader,
                    quant_format=QuantFormat.QDQ,
                    per_channel=quant_channel_bool)
    print('Calibrated and quantized model saved.')
