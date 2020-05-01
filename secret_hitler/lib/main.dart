import 'package:flutter/material.dart';
import 'dart:math';
import 'package:sprintf/sprintf.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {

    return MaterialApp(    // Title, Theme, Home:
      theme: ThemeData(
//        primarySwatch: Colors.purple
      primaryColor: Colors.purple
      ),
      home: MainPage()
    );
  }
}

class MainPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold( // appBar
      appBar: AppBar( // Title,
        title: Text("Secret Hitler"),
        centerTitle: true,
      ),
      body: Center(
        child: Column( // mainAxisAlignment, children
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: <Widget>[
            getButton(context, "Instructions", () {
              Navigator.push(context, MaterialPageRoute(
                builder: (context) => Instructions()
              ));
            }),
            getButton(context, "Draw a Policy", () {
              Navigator.push(context, MaterialPageRoute(
                builder: (context) => Board()
              ));
            })
          ],
        ),
      ),
    );
  }
}

class Instructions extends StatelessWidget{

  @override
  Widget build(BuildContext context) {
    return Scaffold(    // appBar, body
      appBar: AppBar(
        title: Text("Instructions",
          style: TextStyle(fontSize: 24)
        ),
        backgroundColor: Colors.redAccent
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: <Widget>[
            Text("Gameplay"),
            Text("App Specific Stuff"),
            getButton(context, "Return to Main Menu", () {
              Navigator.pop(context);
//              Navigator.push(context, MaterialPageRoute(
//                builder: (context) => MainPage()
//              ));
            }),
          ]
        ),
      ),
    );
  }
}


class Board extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return BoardState();
  }
}

class BoardState extends State<Board> {
  final fascistColor = Colors.deepOrange;
  final liberalColor = Colors.indigo;
  static var policy = new Policies();
  static var revealedPolicies = ["Void", "Void", "Void"];
  static var policyColors = [Colors.grey, Colors.grey, Colors.grey];
  var fasPolToWin = 6;
  var libPolToWin = 5;
  var selectRejectFlag = false;
  var fasPolInPlay = 0;
  var libPolInPlay = 0;
  static var invalidSelection;

  var buttonText = "Draw Policy";

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text( "Secret Hitler",
          style: TextStyle(fontSize: 24),
        ),
        centerTitle: true,
      ),
      body: Column(
        children: <Widget>[
          Spacer(flex: 1),
          Row(    // GameBoard
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget> [
              getPolicyBoard(fascistColor, Colors.orange, 3, 3, fasPolInPlay),
              getPolicyBoard(liberalColor, Colors.lightBlue, 1, 4, libPolInPlay),
            ]
          ), // GameBoard
          Spacer(flex: 1),
          Row(  // Policy Cards
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget> [
              getPolicyCard(revealedPolicies[0], policyColors[0], 0),
              getPolicyCard(revealedPolicies[1], policyColors[1], 1),
              getPolicyCard(revealedPolicies[2], policyColors[2], 2),
            ]
          ), // Policy Cards
          Spacer(flex: 1),
          ButtonTheme(  // Draw Policy
            minWidth: 120.0,
            height: 50.0,
            child: RaisedButton(
              textColor: Colors.black,
              color: Colors.lightBlue,
              child: Text(
                buttonText,
                style: TextStyle(fontSize: 18),
              ),
              shape: RoundedRectangleBorder(
                side: BorderSide(
                  color: Colors.blue,
                  width: 3.0,
                ),
                borderRadius: BorderRadius.all(Radius.circular(10)),
              ),
              onPressed: () {
                policy.drawPolicies();
                revealedPolicies = policy.revealPolicies();
                policyColors = policy.revealColors();
                selectRejectFlag = true;
                invalidSelection = 5;
                setState(() {});
              },
            )
          ),
          Spacer(flex: 1),
        ]

      )
    );
  }

  Widget getPolicyBoard(var primaryColor, var secondaryColor, var numPrimary, var numSecondary, var polInPlay) {
    var policyTiles = List<Widget>();

    for (var tile = 0; tile < numSecondary; tile++) {
      if (tile < polInPlay) {
        policyTiles.add(getFilledBoardTile(primaryColor));
      } else {
        policyTiles.add(getBoardTile(secondaryColor));
      }
    }
    for (var tile = 0; tile < numPrimary; tile++) {
      if (tile < (polInPlay - numSecondary)) {
        policyTiles.add(getFilledBoardTile(primaryColor));
      } else {
        policyTiles.add(getBoardTile(primaryColor));
      }
    }

    return Padding(
      padding: EdgeInsets.all(2.0),
      child: Container(
          color: Colors.brown,
          width: 130.0,
          height: 350.0,
          child: Padding(
            padding: EdgeInsets.all(8.0),
            child: Container(
              color: primaryColor, //Colors.deepOrange,
              child: Padding(
                padding: EdgeInsets.all(15.0),
                child: Container(
                  color: Colors.yellowAccent,
                  child: Padding(
                    padding: EdgeInsets.all(3.0),

                    child: Column(
                      children: policyTiles
                    ),
                  ),
                ),
              ),
            ),
          )
      ),
    );
  }

  Widget getBoardTile (var color) {
    return Flexible(
      child: Padding(
        padding: EdgeInsets.fromLTRB(0.0, 0.0, 0.0, 0.5),
        child: Container(
          color: color,
        ),
      ),
    );
  }

  Widget getFilledBoardTile(var color) {
    var text;
    if (color == fascistColor) {
      text = "F";
    } else {
      text = "L";
    }

    return Flexible(
      child: RotatedBox(
        quarterTurns: 3,
        child: getPolicyCard(text, color, 2)
      )
    );
  }

  Widget getPolicyCard(String policyType, var policyColor, var number) {
    var validSelections = true;

    return  InkWell(
      onTap: () {
        if (number != invalidSelection) {
          if (selectRejectFlag) {
            policyColors[number] = Colors.grey;
            revealedPolicies[number] = "X";
            selectRejectFlag = false;
            invalidSelection = number;
            setState(() {});
          } else {
            addPolicyToBoard(policyColors[number], revealedPolicies[number]);
            selectRejectFlag = true;
            policyColors = [Colors.grey, Colors.grey, Colors.grey];
            revealedPolicies = ["X", "X", "X"];
            invalidSelection = 5;
            setState(() {});
          }
        }
      },
      child:Padding(
          padding: EdgeInsets.all(4.0),
        child: Container(
          color: Colors.black,
          width: 55.0,
          height: 80.0,
          child: Padding(
            padding: EdgeInsets.all(0.5),
            child: Container(
              color: Colors.yellow[50],
              child: Padding(
                padding: EdgeInsets.all(5.0),
                child: Container(
                  color: policyColor,
                  child: Padding(
                    padding: EdgeInsets.all(5.0),
                    child: Container(
                      color: Colors.yellow[50],
                      child: Center(
                        child: RotatedBox(
                          quarterTurns: 0,
                          child: Text(
                            policyType,
                            style: TextStyle(
                              fontSize: 18,
                              color: policyColor,
                            ),
                          ),
                        ),
                      ),
                    )
                  )
                )
              )
            )
          )
        )
      )
    );
  }

  void addPolicyToBoard(var policyColor, var policyText) {
    if (policyColor == fascistColor) {
      fasPolInPlay++;
    } else if (policyColor == liberalColor) {
      libPolInPlay++;
    } else {
      print("Error - invalid policy type");
    }
    if ( (fasPolInPlay >= fasPolToWin) || (libPolInPlay >= libPolToWin)) {
      fasPolInPlay = 0;
      libPolInPlay = 0;
    }
  }
}

Widget getButton(BuildContext context, String text, VoidCallback callback) {
  return ButtonTheme(
    minWidth: 300,
    height: 80,
    child: RaisedButton(
      textColor: Colors.black,
      color: Colors.greenAccent,
      child: Text(
          text,
          style: TextStyle(fontSize: 24)
      ),
      shape: RoundedRectangleBorder(
        side: BorderSide(
          color: Colors.blue,
          width: 5,
        ),
        borderRadius: BorderRadius.all(Radius.circular(30)),
      ),
      onPressed: callback,
    ),
  );
}

class Policies {
  /* Deck of policy cards.
      Used to randomly draw three policy cards     */

  static var numLiberal = 6;
  static var numFascist = 11;
  static var policies = ["Void", "Void", "Void"];
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
    for(int i = 0; i < 3; i++) {
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
