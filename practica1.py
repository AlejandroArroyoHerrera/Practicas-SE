class Perceptron:
    def _init_(self, num_inputs):
        self.weigths = [random.uniform(-1,1)for _ in range(num_inputs)]
        self.bias = random.uniform(-1,1)

    def predict(self, inputs):
        activation = self.bias
        for i in range(len(inputs)):
            activaiton  += inputs[i]*self.weigths[i]
        return 1 if activation >= 0 else 0
    
    def train(self, inputs, target):
        output = self.predict(inputs)
        error = target - output
        self.bias += error 
        for i in range(len(self.weigths)):
            self.weigths[i] += error * inputs[i]

    def get_weigths(self):
        return self.weigths
    
#    def save_weigths(self, filename):
#       with open()

