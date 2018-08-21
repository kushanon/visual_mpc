from .general_agent import GeneralAgent
import pickle as pkl
import numpy as np
import cv2
import os
import shutil
import pdb


class BenchmarkAgent(GeneralAgent):
    def __init__(self, hyperparams):
        self._start_goal_confs = hyperparams.get('start_goal_confs', None)
        self.ncam = hyperparams['env'][1].get('ncam', 2)
        GeneralAgent.__init__(self, hyperparams)
        self._is_robot_bench = 'robot_name' in self._hyperparams['env'][1]

    def _setup_world(self, itr):
        self._reset_state = self._load_raw_data(itr)
        GeneralAgent._setup_world(self, itr)

    def _required_rollout_metadata(self, agent_data, traj_ok, t):
        GeneralAgent._required_rollout_metadata(self, agent_data, traj_ok, t)
        point_target_width = self._hyperparams.get('point_space_width', self._hyperparams['image_width'])
        ntasks = self._hyperparams.get('ntask', 1)
        agent_data['stats'] = self.env.eval(point_target_width, self._hyperparams.get('_bench_save', None), ntasks)

        if not traj_ok and self._is_robot_bench:
            """
            Hot-wire traj_ok to give user chance to abort experiment on failure
            """
            print('WARNING TRAJ FAILED')
            if 'n' in raw_input('would you like to retry? (y/n): '):
                agent_data['traj_ok'] = True

    def _init(self):
        if self._is_robot_bench:
            if os.path.exists(self._hyperparams['_bench_save']):
                shutil.rmtree(self._hyperparams['_bench_save'])
            os.makedirs(self._hyperparams['_bench_save'])

            ntasks = self._hyperparams.get('ntask', 1)

            if 'register_gtruth' in self._hyperparams and len(self._hyperparams['register_gtruth']) == 2:
                goal_image, self._goal_obj_pose = self.env.get_obj_desig_goal(self._hyperparams['_bench_save'], True,
                                                                              ntasks=ntasks)
                self._goal_image = goal_image.astype(np.float32) / 255.
            else:
                self._goal_obj_pose = self.env.get_obj_desig_goal(self._hyperparams['_bench_save'], ntasks=ntasks)
            GeneralAgent._init(self)
            return

        self.env.set_goal_obj_pose(self._goal_obj_pose)
        GeneralAgent._init(self)

    def _load_raw_data(self, itr):
        """
        doing the reverse of save_raw_data
        :param itr:
        :return:
        """
        if 'robot_name' in self._hyperparams['env'][1]:   # robot experiments don't have a reset state
            return None

        ngroup = 1000
        igrp = itr // ngroup
        group_folder = '{}/traj_group{}'.format(self._start_goal_confs, igrp)
        traj_folder = group_folder + '/traj{}'.format(itr)

        print('reading from: ', traj_folder)
        if 'num_load_steps' in self._hyperparams:
            num_images = self._hyperparams['num_load_steps']
        else:
            num_images = 2

        obs_dict = {}
        goal_images = np.zeros([num_images, self.ncam, self._hyperparams['image_height'], self._hyperparams['image_width'], 3])
        for t in range(num_images):  #TODO detect number of images automatically in folder
            for i in range(self.ncam):
                goal_images[t, i] = cv2.imread('{}/images{}/im_{}.png'.format(traj_folder, i, t))[...,::-1]
        self._goal_image = goal_images.astype(np.float32)/255.

        with open('{}/agent_data.pkl'.format(traj_folder), 'rb') as file:
            agent_data = pkl.load(file)
        with open('{}/obs_dict.pkl'.format(traj_folder), 'rb') as file:
            obs_dict.update(pkl.load(file))
        reset_state = agent_data['reset_state']

        self._goal_obj_pose = obs_dict['object_qpos'][-1]

        return reset_state
