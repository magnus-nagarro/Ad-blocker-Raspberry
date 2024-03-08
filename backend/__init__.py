from flask import Flask, jsonify, request, Response, logging, current_app
from pymongo import MongoClient

# own modules
from MongoDB import mongodb
