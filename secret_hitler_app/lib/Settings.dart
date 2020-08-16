import 'dart:math';
import 'package:flutter/material.dart';

class Settings {
  static var numPlayers;
  static List<String> playerNames;
  static List<String> roles = [];
  static List<String> presidentialPowers = [];

  // static List<String> presidentialPowers;

  static var numFas;
  static var numLib;

  static var setupFlag = true;

  void setSettings(var number, List<String> names) {
    setupFlag = false;
    numPlayers = number;
    playerNames = names;

    switch (numPlayers) {
      case 5:
        {
          numLib = 3;
          numFas = 1;
          break;
        }
      case 6:
        {
          numLib = 4;
          numFas = 1;
          break;
        }
      case 7:
        {
          numLib = 4;
          numFas = 2;
          break;
        }
      case 8:
        {
          numLib = 5;
          numFas = 2;
          break;
        }
      case 9:
        {
          numLib = 5;
          numFas = 3;
          break;
        }
      case 10:
        {
          numLib = 6;
          numFas = 3;
          break;
        }
      default:
        {
          print("Error! Invalid Number of Players: $numPlayers");
          break;
        }
    }
    assignRoles();
  }

  void assignRoles() {
    Random random = new Random();
    int randomNumber;
    var fasCount = numFas;
    var libCount = numLib;
    var hitlerCount = 1;
    var playerCount = numPlayers;

    for (var i = 0; i < numPlayers; i++) {
      randomNumber = random.nextInt(playerCount);
      if (randomNumber < hitlerCount) {
        hitlerCount--;
        roles.add('Hitler');
      } else if (randomNumber < (libCount + hitlerCount)) {
        libCount--;
        roles.add('Liberal');
      } else {
        fasCount--;
        roles.add('Fascist');
      }
      playerCount--;
    }

//    for (var i = 0; i < numPlayers; i++) {
//      String playerName = playerNames[i];
//      String role = roles[i];
//      print("$playerName: $role\n");
//    }
  }

  bool isSetup() {
    return !setupFlag;
  }

  List<String> getNames() {
    return playerNames;
  }

  int getNumPlayers() {
    return numPlayers;
  }

  int getNumFas() {
    return numFas;
  }

  int getNumLib() {
    return numLib;
  }

  String getPlayerName(int index) {
    return playerNames[index];
  }

  String getPlayerRole(int index) {
    return roles[index];
  }
}
