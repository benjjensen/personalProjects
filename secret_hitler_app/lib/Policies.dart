import 'package:flutter/material.dart';
import 'dart:math';

class Policies {
  /* Deck of policy cards.
      Used to randomly draw three policy cards     */

  static var numLiberal = 6;
  static var numFascist = 11;
  static var policies = ["", "", ""];
  static var colors = [Colors.grey, Colors.grey, Colors.grey];

  void reshufflePolicies() {
    // Resets the number of liberal and fascist policies
    numLiberal = 6;
    numFascist = 11;
  }

  void drawPolicies() {
    /*  Updates policies with three new policy cards
        Samples and updates the liberal/fascist card distribution
        Shuffles when necessary     */

    Random random = new Random();
    int numPolicies = numLiberal + numFascist;
    int randomNumber;
    if (numPolicies < 3) {
      reshufflePolicies();
      numPolicies = 17;
      policies[0] = "RS";
      policies[1] = "RS";
      policies[2] = "RS";
      colors[0] = Colors.green;
      colors[1] = Colors.green;
      colors[2] = Colors.green;
      return;
    }
    for (int i = 0; i < 3; i++) {
      randomNumber = random.nextInt(numPolicies);
      if (randomNumber < numFascist) {
        numFascist -= 1;
        policies[i] = "F";
        colors[i] = Colors.deepOrange;
      } else {
        numLiberal -= 1;
        policies[i] = "L";
        colors[i] = Colors.indigo;
      }
      numPolicies -= 1;
    }
  }

  List revealPolicies() {
    return policies;
  }

  List revealColors() {
    return colors;
  }
}
