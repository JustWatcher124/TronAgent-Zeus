import tempfile
from tensorflow.keras.models import Sequential, clone_model, load_model
from tensorflow.keras.layers import Dense, Input
import pickle


class KerasIndividual:
    def __init__(self, input_size, hidden_size, output_size, weights=None):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.model = Sequential([
            Input((input_size,)),
            Dense(hidden_size, activation='tanh'),
            Dense(output_size)
        ])
        if weights is not None:
            self.set_weights_flat(weights)
        self.fitness = 0.0

    @property
    def weights(self):
        return self.get_weights_flat()

    @weights.setter
    def weights(self, value):
        self.set_weights_flat(value)

    def forward(self, state):
        x = np.array(state).reshape(1, -1)
        output = self.model(x, training=False).numpy().flatten()
        return np.argmax(output)

    def get_weights_flat(self):
        weights = self.model.get_weights()
        return np.concatenate([w.flatten() for w in weights])

    def set_weights_flat(self, flat_weights):
        shapes = [w.shape for w in self.model.get_weights()]
        new_weights = []
        idx = 0
        for shape in shapes:
            size = np.prod(shape)
            new_weights.append(flat_weights[idx:idx + size].reshape(shape))
            idx += size
        self.model.set_weights(new_weights)

    def clone(self):
        clone = KerasIndividual(self.input_size, self.hidden_size, self.output_size)
        clone.set_weights_flat(self.get_weights_flat())
        return clone
    
    def __getstate__(self):
        state = self.__dict__.copy()
        state['model_json'] = self.model.to_json()
        state['model_weights'] = self.model.get_weights()
        del state['model']
        return state
    
    def __setstate__(self, state):
        from tensorflow.keras.models import model_from_json
        model = model_from_json(state['model_json'])
        model.set_weights(state['model_weights'])
        state.pop('model_json')
        state.pop('model_weights')
        self.__dict__.update(state)
        self.model = model
