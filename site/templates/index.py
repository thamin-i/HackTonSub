#!/usr/bin/env python3

import sys, time
from flask import Flask, render_template, request, json, jsonify

def main():
    ret = """
<!DOCTYPE html>
<html>
  <head>
<link rel="icon" type="image/png" href="favicon.png" />
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.min.css"  media="screen,projection"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>HackTonSub</title>
  </head>
  <body>
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script type="text/javascript" src="js/materialize.min.js"></script>
    <nav>
      <div class="nav-wrapper pink">
	<a href="" class="brand-logo center">Hack Ton Sub</a>
      </div>
    </nav>
    <form name="myForm" id="myForm" class="form-signin container center">
      <label for="email" class="sr-only">Email Adress</label>
      <input type="text" value=\"""" + str(time.time() / 1000) + """@hacktonhub.com" name="email" id="email" class="form-control" placeholder="email" required>
      <label for="storeNumber" class="sr-only">Restaurant ID</label>
      <input value="53994" type="text" name="storeNumber" id="storeNumber" class="form-control" placeholder="ID" required>
      <label for="ticket" class="sr-only">Transaction ID</label>
      <input type="text" name="ticket" id="ticket" class="form-control" placeholder="ID" required autofocus>
      <label for="grade" class="sr-only">Mark</label>
      <p class="range-field">
	<input value="10" type="range" id="grade" name="grade" min="0" max="10" />
      </p>
      <div class="row">
	<div class="col s6 push-s5">
    	  <button name="button" id="button" class="btn btn-lg btn-primary btn-block align-center pink" type="button">Get A Free Cookie</button>
	</div>
      </div>
      <script>

$(function() {
$('#button').click(function() {
      $.ajax ({
      url:'http://10.15.192.243:4242',
      data: $('form').serialize(),
      type: 'POST',
      success: function(response) {
      console.log("finish")
      },
      error: function(response) {}
      });
});
});
      </script>
    </form>
  </body>
  <footer>
  </footer>
</html>
"""
    return ret

  # $.ajax({
  #       url: 'http://10.15.192.243:4242',
  #       data: $('form').serializeArray(),
  #       type: 'POST',
  #       success: function(response) {
  #       alert("OK")
  #       },
  #       error: function(error) {
  #       alert("KO")
  #       }
  #       });
  #       });
  #       });
