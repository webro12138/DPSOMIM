import random
from tqdm import tqdm
from algorithm import AlgorithmBase
import numpy as np
class Particle:
    def __init__(self, position, best_position, best_fitness, velocity):
        self.position = position
        self.velocity = velocity
        self.best_position = best_position
        self.best_fitness = best_fitness
        

    def update_position(self, search_space):
   
        for i in range(len(self.velocity)):
            temp = list(set(search_space) - set(self.position))
            if(self.velocity[i] == 1 and temp != []):
                self.position[i] = random.choice(temp)

    def update_velocity(self, global_best_position, w, c1, c2):
      
        for i in range(len(self.velocity)):
            r1 = random.uniform(0, 1)
            r2 = random.uniform(0, 1)
   
            if(self.position[i] in self.best_position):
                temp = 0
            else: 
                temp = 1
            
            
            cognitive = c1 * r1 * temp 
            
            if(self.position[i] in global_best_position):
                temp = 0
            else: 
                temp = 1
            
            
            social = c2 * r2 *  temp
            
            if(w * self.velocity[i] + cognitive + social > 1):
                self.velocity[i] = 1
            else:
                self.velocity[i] = 0
    
    def evaluate_fitness(self, network, diffusion_model):
        fitness = diffusion_model.approx_func(network, self.position)
        if fitness > self.best_fitness:
            self.best_fitness = fitness
            self.best_position = list(self.position)


class PSOBMIM(AlgorithmBase):
    def __init__(self, diffusion_model, cs_alg=None, beta=0.25, num_particles=100, w=0.8, c1=1.8, c2=1.8, max_iterations=100, is_NO=True, verbose=True, seed=None):
        super().__init__()
        random.seed(seed)
        self.diffusion_model = diffusion_model
        self.cs_alg = cs_alg
        self.num_particles = num_particles
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.max_iterations = max_iterations
        self.beta = beta
        self.particles = []
        self.global_best_position = []
        self.global_best_fitness = 0
        self.is_NO = is_NO
        self.verbose=verbose
        
        self._history = {"name":self._name, "max_iterations":max_iterations,"global_best_fitness":[]}

    def initialize_particles(self):
        
        # self.search_space = list(dict(sorted(self.network.degrees(self.search_space).items(), key=lambda x:x[1], reverse=True)).keys())
       

        for i in range(self.num_particles):
            # if(i == 0):
            #     position = self.search_space[0:self.num_dimensions]
            #     best_position = self.search_space[0:self.num_dimensions]
            # else: 
            position = random.sample(self.search_space, self.num_dimensions)
            best_position = random.sample(self.search_space, self.num_dimensions)
  
                        
            velocity = [0 for _ in range(self.num_dimensions)]
            particle = Particle(position, best_position, self.diffusion_model.approx_func(self.network, best_position), velocity)
            self.particles.append(particle)
            
    

    def set_setting(self, network, k):
        self.reset()
        self.num_dimensions = k
        self.network = network
    

    def Noc(self):
        return int(self.k + (self.network.number_of_nodes() - self.k) * np.power(self.beta * self.k / self.network.number_of_nodes(), 1-self.beta))
    
    def reset(self):
        self.global_best_position = []
        self.global_best_fitness = 0
        self.search_space = []
        self.particles = []
      
        
    def run(self, network, k):
        
        self.set_setting(network, k)
     
        if(self.verbose):
            loop = tqdm(range(self.max_iterations), total = self.max_iterations)
        else:
            loop = range(self.max_iterations)
        
        if(self.cs_alg !=None):
              
              self.search_space = self.cs_alg(self.network, int(k + (self.network.number_of_nodes() - k) * np.power(self.beta * k / self.network.number_of_nodes(), 1-self.beta)))
        else:
            self.search_space = self.network.nodes()
  
        self.initialize_particles()
        self._history["name"] = self.get_name()
        self._history["global_best_fitness"] = []
        for _ in loop:
            for i in range(len(self.particles)):
                # if(i - 1 < 0):
                #     pre_position = self.particles[-1].best_position
                # else: 
                #     pre_position = self.particles[i - 1].best_position 
                
                # if(i + 1 >= len(self.particles)):
                #     nex_position = self.particles[0].best_position
                # else:
                #     nex_position = self.particles[i + 1].best_position     
                
                # pre_position = self.particles[random.randint(0, len(self.particles) - 1)].best_position    
                # nex_position = self.particles[random.randint(0, len(self.particles) - 1)].best_position  
                self.particles[i].update_velocity(self.global_best_position, self.w, self.c1, self.c2)
                self.particles[i].update_position(self.search_space)
            
            
            for particle in self.particles:
                particle.evaluate_fitness(self.network, self.diffusion_model)
                
                if particle.best_fitness > self.global_best_fitness:
                    self.global_best_fitness = particle.best_fitness
                    self.global_best_position = list(particle.best_position)

            
            if(self.is_NO):
                self.local_search()   

            self._history["global_best_fitness"].append(self.global_best_fitness)
            loop.set_description(f"解优化 | fitness {self.global_best_fitness:.4}")
            
        return self.global_best_position
    

    def local_search(self):
        for i in range(len(self.global_best_position)):
            old = self.global_best_position[i]
            neigbours = list(set(self.network.neighbors(old)) - set(self.global_best_position))
            if(len(neigbours)):
                self.global_best_position[i] = random.choice(neigbours)
                fitness = self.diffusion_model.approx_func(self.network, self.global_best_position)
                if(fitness > self.global_best_fitness):
                    self.global_best_fitness = fitness
                else:
                    self.global_best_position[i] = old

    def get_global_best_position(self):
        return self.global_best_position

    def get_global_best_fitness(self):
        return self.global_best_fitness

    def set_beta(self, beta):
        self.beta = beta

    def __history__(self):
        return self._history.copy()

    