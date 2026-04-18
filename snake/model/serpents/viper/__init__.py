# don't think about importing GeneticAlgorithm here, causes a circular import:
#   GeneticAlgorithm -> Model -> serpents -> Viper -> GeneticAlgorithm
from snake.model.serpents.viper.viper import Viper
