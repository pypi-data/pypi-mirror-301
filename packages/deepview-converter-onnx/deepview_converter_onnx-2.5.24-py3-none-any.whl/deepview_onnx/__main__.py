from sys import prefix
from .conversion_onnx import convert_to_onnx
import os
from deepview.converter.plugin_api.args_processor import ArgsProcessor
import tempfile
import shutil



def query_convert(src_type, dst_type):
    try:

        if src_type is None or dst_type is None:
            return {
                'supported_inputs': [{'ext':'h5','name':'Keras'}, {'ext':'pb','name':'Tensorflow'},{'ext':'onnx','name':'ONNX'}],
                'supported_outputs':[{'ext':'onnx','name':'ONNX'}]
            }

        ref = {} 
        if dst_type != 'onnx':
            return None

        ref['onnx-opset']=  {'type': 'int',     'default': 11,'group':'debug','public':True,
                    'help':'Onnx additional operations'}
        if src_type=='h5' or src_type=='pb':
            ref['tflite-converter'] = {'type': 'string','choices': ['mlir','toco'], 'default':'mlir', 'group':'debug','public':True,
                'help':'Converter library to use'}
        
        return ref
    except:
        return None

def convert(infile, outfile, params):
    try:
        args = ArgsProcessor()
        src_type=''
        dst_type=''
   
        if 'output-model-type' in params:
            dst_type = params['output-model-type']
        else:
            dst_type = args.get_dest_type(outfile)
        if 'input-model-type' in params:
            src_type=params['input-model-type']
        else:
            src_type=args.get_source_type(infile)

        
        ref = query_convert(src_type, dst_type)
        if ref is None:
            return {
                'success': 'no',
                'message': 'Not Valid file formats'
            }
        args.process(params,ref)
        
        samples = args.samples.split(',')
        for i in range(len(samples)):
            samples[i] = os.path.abspath(samples[i])
        
        if args.samples.endswith('.deepview') or \
                args.samples.endswith('.eiqp'):
            samples = [args.samples, args.crop]
            samples[0] = os.path.abspath(args.samples)

    except AttributeError as e:
        return {
            'success': 'no',
            'message': "ERROR:"+str(e)
        }

    converter_response={'success':'no','message':''}
    try:
        currentWorkingDir = os.getcwd()
        if os.path.exists(currentWorkingDir + '/' + infile):
            infile = currentWorkingDir + '/' + infile
            outfile = currentWorkingDir + '/' + outfile
            
        tempd = tempfile.TemporaryDirectory(prefix='eIQ_TMP_')
        tempfolder = tempd.name
        print('working in temporary directory:', tempfolder)
        os.chdir(tempfolder)

        default_shape =  args.input_shape

        if args.input_names == '' or args.input_names is None:
            input_names = None
        else:
            input_names = args.input_names

        if args.output_names == '' or args.output_names is None:
            output_names = None
        else:
            output_names = args.output_names
        
        try:
            tflite_converter= args.tflite_converter
        except:
            tflite_converter=None

        onnx_opset=11
        try:
            onnx_opset=int(args.onnx_opset)
        except:
            onnx_opset=11

        convert_to_onnx(infile, outfile, input_names, output_names, samples, args.num_samples,
                            default_shape, args.quant_channel, args.quantize, onnx_opset,
                            args.quant_normalization, tflite_converter)

        converter_response={'success': 'yes','message': 'Converted'}

    except Exception as e:
        converter_response = {  'success': 'no','message': str(e)}
    finally:
        os.chdir(currentWorkingDir)
        shutil.rmtree(tempfolder)

    return converter_response
#  ------------------------------------  Private Functions ---------------------------------------------
def __get_source_type(infile):
    src = ""
    try:
        if os.path.isfile(infile):
            src = os.path.splitext(infile)[1]
            src = src.replace('.', '')
        else:   # it is a dir
            #check for saved model
            for fname in os.listdir(infile):
                if os.path.splitext(fname)[1] == '.pb':
                    src = 'pb'
    except Exception as e:
        print(e)
        src=''
    return src
  
