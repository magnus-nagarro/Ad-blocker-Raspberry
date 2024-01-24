from flask import Flask, jsonify, request, Response, logging
from pymongo import MongoClient

# own modules
from MongoDB import mongodb
