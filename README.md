#### In this repository, I have fullstack projects which uses Flask as a backend.

###### Note : Depoyment over GCP for deep learning app requires addition storage apart from thier free storage limits. This is mainly because of the tensorflow 2.2 package which occupies lot of storage.<br>
##### <b>However, this code is fully functional locally.<b><br>

1. <b>Opening price forecasting webapp.</b>
  * This projects aims at creating an opening price forecast for the next 90 days.
  * It is developed using the Python Flask backend and ReactJS frontend.
  * It takes the dataset from MySQL and get it displayed over the screen and then feeds it for training the LSTM multivariate forecasting model and saves the forecast back into the MySQL.
