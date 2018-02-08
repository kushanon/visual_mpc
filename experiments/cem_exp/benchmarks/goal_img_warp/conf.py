import python_visual_mpc
base_dir = python_visual_mpc.__file__
base_dir = '/'.join(str.split(base_dir, '/')[:-2])

current_dir = '/'.join(str.split(__file__, '/')[:-1])

# local output directory
OUT_DIR = current_dir + '/modeldata'

from python_visual_mpc.video_prediction.dynamic_rnn_model.dynamic_base_model import Dynamic_Base_Model

configuration = {
'experiment_name': 'rndaction_var10',
'pred_model':Dynamic_Base_Model,
'output_dir': OUT_DIR,      #'directory for model checkpoints.' ,
'current_dir': current_dir, #'directory for writing summary.' ,
'pretrained_model': base_dir + '/tensorflow_data/sim/cartgripper/modeldata/model144002',     # 'filepath of a pretrained model to resume training from.' ,
'sequence_length': 15,      # 'sequence length to load, including context frames.' ,
'skip_frame': 1,            # 'use ever i-th frame to increase prediction horizon' ,
'context_frames': 2,        # of frames before predictions.' ,
'use_state': 1,             #'Whether or not to give the state+action to the model' ,
'model': 'cdna',            #'model architecture to use - CDNA, DNA, or STP' ,
'num_transformed_images': 4,   # 'number of masks, usually 1 for DNA, 10 for CDNA, STN.' ,
'schedsamp_k': -1,      # 'The k hyperparameter for scheduled sampling -1 for no scheduled sampling.' ,
'batch_size': 200,           #'batch size for training' ,
'learning_rate': 0.,     #'the base learning rate of the generator' ,
'visualize': '',            #'load model from which to generate visualizations
'file_visual': '',          # datafile used for making visualizations
'kern_size': 17,            # size of DNA kerns
'single_view':"",
'use_len':14,                # number of steps used for training where the starting location is selected randomly within sequencelength
'1stimg_bckgd':'',
'adim':3,
'sdim':6,
'normalization':'in',
'previmg_bckgd':'',
'gen_img':'',
'img_height':48,
'img_width':64,
'use_goal_image':'',
'no_pix_distrib':'',
'use_vel':''                # add the velocity to the state input
}