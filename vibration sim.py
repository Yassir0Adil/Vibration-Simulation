import multiprocessing as mp

def multiprocessing_on_objectList(Mylist,func,*argss):
    processes=[]

    for obj in Mylist:
        processes.append(mp.Process(target=func,args=(obj,argss,)))
    for process in processes:
        process.start
    for process in processes:
        process.join()

class Wall:
    def __init__(self):
        self.displacement=0
        self.velocity = 0

class Mass:
    num_of_masses=0
    list_of_masses=[]

    def __init__(self , mass , v ):
        Mass.num_of_masses += 1
        self.name = f'M{Mass.num_of_masses}'
        self.mass = mass
        self.velocity = v
        self.links={'left':[] ,'right':[]}
        self.displacement=0
        self.path=[self.displacement]
        Mass.list_of_masses.append(self)

    def connect_masses(self,other,direction,Spring,*args):
        spring=Spring(args)

        if direction.lower()=='r' or direction.lower()=='right':
            self.links['right'].append(spring)
            spring.addLinks(other,self)
            #addLink arguments are ordered left, right of the spring

        else:
            other.links['left'].append(spring)
            spring.addLinks(self,other)
    
    @property
    def acceleration(self):
        Lforces=0
        Rforces=0
        
        for object in self.links['left']:
            Lforces+=object.force
        for object in self.links['right']:
            Rforces+=object.force

        F=Lforces-Rforces
        #g=F/mass
        return F/self.mass

    def update_motion(self,dt):
        self.velocity+=self.acceleration*dt
        self.displacement+= self.velocity*dt+self.acceleration*(dt**2)
        self.path.append(self.path[-1]+self.displacement)

    

    @classmethod
    def updateAllMasses(cls,dt):
        for mass in cls.list_of_masses:
            mass.update_motion(dt)

    def __str__(self):
        return self.name
    
    

class Spring:
    num_of_springs=0
    list_of_springs=[]

    def __init__(self,k,dl=0,b=0):
        Spring.num_of_springs +=1
        self.name=f'spring{Spring.num_of_springs}'
        self.stiffness=k
        self.damping=b
        self.compression=dl
        self.ends=[None,None]

        Spring.list_of_springs.append(self)

    @property
    def force(self):
        #when spring is in compression force is positive
        #forces pointing to the right are positive
        s=self.stiffness
        c=self.compression
        left , right = self.ends
        return (s*c - (left.velocity- right.velocity)  )

    def update_compression(self):
        #motion to the right is positive
        left, right=self.ends
        self.compression+= left.displacement - right.displacement

    def addLinks(self,obj1,obj2):
        self.ends=[obj1,obj2]

    def __str__(self):
        return self.name


class System:
    dt= 0.01
    def __init__(self,runtime,masses):
        self.runtime=runtime
        self.masses=masses

    @classmethod
    def set_dt(cls,dt):
        cls.dt=dt
    
    def step_solver(self):

        multiprocessing_on_objectList(Mass.list_of_masses,Mass.update_motion,System.dt)
        multiprocessing_on_objectList(Spring.list_of_springs,Spring.update_compression)

    def run_sim(self):
        for dt in range(int(self.runtime/self.dt)):
            self.step_solver()


if __name__ == '__main__':
    pass
    
