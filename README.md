## Codes for MCM
#### Team 2428217 
#### Problem B
# Code for Task 1:
>- [Submersible_motion_model.py](https://github.com/Higasa-Yumetaka/MCM_Control_Number_2428217_Python/blob/master/Submersible_motion_model.py)\
> Dynamic simulation of a submersible in Task 1, running this file separately will simulate the descent path of a submersible.\
> ![submersible_motion](https://github.com/Higasa-Yumetaka/MCM_Control_Number_2428217_Python/blob/master/Pictures/predicted_path.png)

# Code for Task 2:
>- [MatLab_Codes/task2.m](https://github.com/Higasa-Yumetaka/MCM_Control_Number_2428217_Python/blob/master/MatLab_Codes/task2.m)\
> We have considered several devices for underwater search and assigned attributes with corresponding scores to each of them. Using AHP, we determined the relationships between these attributes and calculated the cost-efficiency ratio for each device as a score. Subsequently, we selected the top-scoring devices to be mounted on the host ship.
>- [AHP2.py](https://github.com/Higasa-Yumetaka/MCM_Control_Number_2428217_Python/blob/master/AHP2.py)\
> Analytic Hierarchy Process:By inputting the matrix of importance relationships, we calculated the importance coefficients between various attributes, which serve as the factors for scoring.
> ![importance_matrix](https://github.com/Higasa-Yumetaka/MCM_Control_Number_2428217_Python/blob/master/Pictures/importance_matrix.jpg)

# Code for Task 3:
>- [Monte_Carlo_simulation.py](https://github.com/Higasa-Yumetaka/MCM_Control_Number_2428217_Python/blob/master/Monte_Carlo_simulation.py)\
> The preceding code *[Submersible_motion_model.py](https://github.com/Higasa-Yumetaka/MCM_Control_Number_2428217_Python/blob/master/Submersible_motion_model.py)* can simulate the future positions of a submersible for a certain period, allowing for the calculation of its final resting position. However, this only reflects a single scenario. To devise a search plan, we need to understand the probability of the submersible appearing at each location. To achieve this, we conducted 20,000 simulations of the submersible's route using Monte Carlo simulation. We aggregated the final resting positions from all simulations to provide data for calculating the probability density of the submersible's locations.
>- [kde.py](https://github.com/Higasa-Yumetaka/MCM_Control_Number_2428217_Python/blob/master/kde.py)\
>- We used Kernel Density Estimation (KDE) to analyze these data to understand its probability distribution and facilitate subsequent search planning.\
> ![Kernel_Density_Estimation](https://github.com/Higasa-Yumetaka/MCM_Control_Number_2428217_Python/blob/master/Pictures/kde.png)
>- [MatLab_Codes/task3.m](https://github.com/Higasa-Yumetaka/MCM_Control_Number_2428217_Python/blob/master/MatLab_Codes/task3.m)\
> We chose the point with the highest probability density as the starting point and employed the Archimedean spiral as the search route. This way, our search progresses from the location with the highest probability towards lower probability areas. This program visualizes the search route, aiding in understanding the path. You can also use Python to execute *[search_plan_plt.py](https://github.com/Higasa-Yumetaka/MCM_Control_Number_2428217_Python/blob/master/search_plan_plt.py)* for visualizing this route.\
> ![search_plan](https://github.com/Higasa-Yumetaka/MCM_Control_Number_2428217_Python/blob/master/Pictures/search_route.png)
>- [search_Probability.py](https://github.com/Higasa-Yumetaka/MCM_Control_Number_2428217_Python/blob/master/search_Probability.py)\
> Based on the probability density distribution obtained before, we decided to search from the point with the highest probability using the Archimedean spiral as the trajectory. This search method will start from the position with the highest probability and continue to search to the position with lower probability. The program searches in this manner and generates a relationship between the probability of finding the submersible and the time spent searching.

# Code for Task 4:
>- [MatLab_Codes/multiple.m](https://github.com/Higasa-Yumetaka/MCM_Control_Number_2428217_Python/blob/master/MatLab_Codes/multiple.m)\
> Our model *[Submersible_motion_model.py](https://github.com/Higasa-Yumetaka/MCM_Control_Number_2428217_Python/blob/master/Submersible_motion_model.py)* can initialize different environmental parameters to simulate different sea areas, while model *[Monte_Carlo_simulation.py](https://github.com/Higasa-Yumetaka/MCM_Control_Number_2428217_Python/blob/master/Monte_Carlo_simulation.py)* can specify how many submersibles to simulate in a neighboring area. This program simulates how to search for these submersibles in a faster route when there are multiple submersibles in an adjacent range.