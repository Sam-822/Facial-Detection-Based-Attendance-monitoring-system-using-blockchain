# Real-time Attendance Monitoring System using Machine Learning and Blockchain

The project aims to provide a solution to the attendance management problem by implementing a facial recognition based attendance monitoring system that stores the attendance records over a blockchain network.
## Deployment

In order to run this project, you will need XAMPP, Ganache, Truffle suite, CMake, Nodejs

Follow the steps from [here](https://www.geeksforgeeks.org/login-and-registration-project-using-flask-and-mysql/) to create the MySQL login database.

Install CMake from [here](https://cmake.org/download/).

Install all the packages required for the project by opening a command prompt from the project directory and running the following command:

```bash
  pip install -r requirements.txt
```
In case some libraries are not installed, install the libraries manually using the command
```bash
  pip install "library_name" --user
 ```

Install NodeJs from the [official website](https://nodejs.org/en/download) to install nvm and npm.

Follow the steps shown [here](https://trufflesuite.com/docs/truffle/how-to/install/) to install truffle suite.

Download Ganache from the [official website](https://trufflesuite.com/ganache/)

Run ganache, quickstart a blockchain network, go to settings, change the port number under "Server" to "8545", enable "Automine" and under the workspace tab click on "add project" and select the `truffle_config.js` file from the project directory.

Go to the project root directory, open a command prompt in the directory and run the following command:
```bash
  truffle migrate --reset
```
The above command will generate instances of the smart contract on the ganache network, copy the contract address of "2_deploy_agent.js" and paste it in the app.py file.

To run the project on a local host, run the following command:
```bash
  python app.py
```



## Authors

- [@Abdul Samad](https://github.com/Sam-822)
- [@Sindura Dasi](https://github.com/sinduraDasi)
- [@Ekta Gujar](https://github.com/ekta1000)

