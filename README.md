# Thermique appart
Ensemble de script python pour étudier et modéliser le comportement thermique de mon appartement.


## Sources de données météo
 * https://darksky.net/dev/docs
 * https://www.meteoblue.com/fr/meteo/archive/export
 
 
## Calcul du flux solaire
 * librairie Pysolar: http://pysolar.org/
 
### Calcul de l'horizon
... pour avoir une bonne estimation du levé et couché de soleil (je n'habite pas en plaine).
[notebook horizon](./ombres_montagnes.ipynb)

## Fusion des données : 
[notebook preprocess](./get_data_and_preprocess.ipynb)


# Modèle de la température des tuiles
[notebook tuile](./Model02_tuile.ipynb)
<img src="./images/sch_model02.jpg" width="450px" alt='schema mod02' />


# Modèle type boite-noire de l'appartement
[notebook blackbox](./BlackBoxModel02.ipynb)



# Références trouvées & intéressantes

* **Estimation of continuous-time models for the heat dynamics of a building.** Energy and Buildings, 22(1), 67-79. Madsen, H., & Holst, J. (1995). [pdf](http://henrikmadsen.org/wp-content/uploads/2014/05/Journal_article_-_1995_-_Estimation_of_continuous-time_models_for_the_heat_dynamics_of_a_building.pdf)


