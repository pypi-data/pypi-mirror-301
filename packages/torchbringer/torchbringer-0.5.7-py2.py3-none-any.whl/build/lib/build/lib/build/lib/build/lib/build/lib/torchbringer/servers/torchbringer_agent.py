import os
import time
from time import gmtime, strftime
import torchbringer.components.builders as builders
import torch

from aim import Run

# if GPU is to be used
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class TorchBringerAgent():
    def __init__(self, verbose=True) -> None:
        self.verbose = verbose

        self.learner = None
        self.config = None
        self.elapsed_time = 0
        self.elapsed_memory_time = 0
    

    def initialize(self, config):
        time_i = time.time_ns()

        data = None
        if "load_path" in config and os.path.isfile(f"checkpoints/{config['load_path']}.pkl"):
            self.elapsed_time += time.time_ns() - time_i
            time_i = time.time_ns()

            data = torch.load(f"checkpoints/{config['load_path']}.pkl")
            config = data["config"]

            self.elapsed_memory_time += time.time_ns() - time_i
            time_i = time.time_ns() 

        self.config = config

        self.save_every_steps = config["save_every_steps"] if "save_every_steps" in config else 0
        self.save_path = config["save_path"] if "save_path" in config else "unnamed"
        self.run = None
        self.cummulative_loss = 0.0
        self.cummulative_reward = 0.0
        self.episode_steps = 0
        self.step_counter = 0
        self.episode_counter = 1 if data is None else data["episode_counter"]
        if "run_name" in config:
            if "run_hash" in config:
                self.run = Run(experiment=config["run_name"], run_hash=config["run_hash"])
            else:
                self.run = Run(experiment=config["run_name"])
                self.config["run_hash"] = self.run.hash
            self.run["hparams"] = config
        
        self.learner = builders.build_learner(config)

        if not data is None:
            self.learner.load_checkpoint(data["checkpoint"])
        
        self.elapsed_time += time.time_ns() - time_i


    def step(self, state, reward, terminal):
        time_i = time.time_ns()

        self.learner.experience(state, reward, terminal)
        self.learner.optimize()

        if not self.run is None:
            self.cummulative_reward += reward
            self.cummulative_loss += self.get_past_loss()
            self.episode_steps += 1
            if terminal:
                self.run.track({"Episode reward": self.cummulative_reward, "Average loss": self.cummulative_loss / self.episode_steps}, step=self.episode_counter)
                self.cummulative_reward = 0.0
                self.cummulative_loss = 0.0
                self.episode_steps = 0
                self.episode_counter += 1
        
        if self.save_every_steps > 0:
            self.step_counter += 1
            if self.step_counter == self.save_every_steps:
                self.elapsed_time += time.time_ns() - time_i
                time_i = time.time_ns()

                self.step_counter = 0
                self.save(self.save_path)

                self.elapsed_memory_time += time.time_ns() - time_i
                time_i = time.time_ns()
                
        ret_val = torch.tensor([], device=device) if state is None else self.learner.select_action(state)

        self.elapsed_time += time.time_ns() - time_i
        if terminal and self.verbose:
            print("Finished episode - Agent elapsed: {:.3f}; Memory time: {:.3f}".format(float(self.elapsed_time) / 10**9, float(self.elapsed_memory_time) / 10**9))

        return ret_val
    

    def save(self, path):
        to_save = {
            "config": self.config,
            "episode_counter": self.episode_counter,
            "checkpoint": self.learner.get_checkpoint_dict()
        }

        if not os.path.exists("checkpoints"):
            os.makedirs("checkpoints")

        torch.save(to_save, f"checkpoints/{path}.pkl")
        torch.save(to_save, f"checkpoints/{path}_backup.pkl")

        if self.verbose:
            print(f"Saved checkpoint {path} @ {strftime('%Y-%m-%d %H:%M:%S', gmtime())}")



    def get_past_loss(self):
        if hasattr(self.learner, "past_loss"):
            return self.learner.past_loss
        return 0.0