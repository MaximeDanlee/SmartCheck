# SmartCheck

## Introduction

SmartCheck is an application designed to breathe new life into discarded smartphones, specifically Fairphone2. These modular phones, developed by the Dutch company Fairphone, are easily repairable, making them ideal candidates for refurbishment and reuse. 

The application diagnoses every component/service of a Fairphone2, providing a comprehensive report on the phone's condition through an intuitive GUI. This project is in partnership with Swarn, an eco-responsible company that uses recycled Fairphone2 to provide environmentally friendly solutions. 

SmartCheck also establishes a collaboration with Village n°1, a support and services organization for disabled people based in Braine-l'Alleud, Belgium. The application is designed to be as suitable and accessible as possible for people with disabilities, automating the testing process as much as possible and providing an intuitive user interface.

## Project Structure

The project is divided into two main parts: the frontend and the backend.

### Frontend

The frontend of the application is built using React, a popular JavaScript library for building user interfaces. The frontend is responsible for presenting the user with an intuitive and easy-to-use interface for running tests and viewing results.

The frontend code is located in the `frontend` directory. This directory contains all the React components, styles, and assets used in the frontend of the application.

### Backend

The backend of the application is built using Python and Flask, a lightweight web server framework. The backend is responsible for running the actual tests on the Fairphone2 devices and reporting the results back to the frontend.

The backend code is located in the `backend` directory. This directory contains the Python scripts for running the tests, as well as the Flask server code.

## Getting Started

To run the application, you will need to set up both the frontend and the backend. Detailed instructions for setting up and running the application can be found in the README files in the `frontend` and `backend` directories.

## Conclusion

SmartCheck is a powerful tool for diagnosing and refurbishing Fairphone2 devices. By automating the testing process and providing an intuitive user interface, SmartCheck makes it easy to give discarded phones a second life, helping to reduce electronic waste and provide jobs for people with disabilities.