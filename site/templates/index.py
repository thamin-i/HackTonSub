#!/usr/bin/env python3

import sys, time
from flask import Flask, render_template, request, json, jsonify

def main():
    ret = """
<!DOCTYPE html>
<html>
  <head>
    <link rel="icon" href="static/favicon.ico" />
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.min.css"  media="screen,projection"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>HackTonSub</title>
  </head>
  <body>
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script type="text/javascript" src="js/materialize.min.js"></script>
    <nav>
      <div class="nav-wrapper blue accent-4">
	<a href="" class="brand-logo center">Hack Ton Sub</a>
      </div>
    </nav>
    <form class="form-signin container center">
      <label for="email" class="sr-only">Email Adress</label>
      <input type="text" value=\"""" + str(time.time() / 1000) + """@hacktonhub.com" name="email" id="email" class="form-control" placeholder="email" required>
      <label for="restaurant" class="sr-only">Restaurant ID</label>
      <input value="53994" type="text" name="restaurant" id="restaurant" class="form-control" placeholder="ID" required>
      <label for="transaction" class="sr-only">Transaction ID</label>
      <input type="text" name="transaction" id="transaction" class="form-control" placeholder="ID" required autofocus>
      <label for="mark" class="sr-only">Mark</label>
      <p class="range-field">
	<input value="5" type="range" id="mark" min="0" max="5" />
      </p>
      <div class="row">
	<div class="col s6 push-s5">
    	  <button id="button" class="btn btn-lg btn-primary btn-block align-center blue accent-4" type="button">Get A Free Cookie</button>
	</div>
      </div>
      <script>
	$(function() {
	$('#button').click(function() {
        $.ajax({
        url: 'https://hacktonsub.api.thamin.ovh',
        data: $('form').serialize(),
        type: 'POST',
        success: function(response) {
	Materialize.toast('OK', 4000, 'green')
        function show_popup(){
        location.reload();
        };
        window.setTimeout( show_popup, 3000 );
        },
        error: function(error) {
	Materialize.toast('KO', 4000, 'red')
	}
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
