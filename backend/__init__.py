from flask import Flask, jsonify, request, Response, logging, current_app
from pymongo import MongoClient
import time as sleep_time

# own modules
from MongoDB import mongodb