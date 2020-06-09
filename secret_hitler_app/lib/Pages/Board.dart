import 'package:flutter/material.dart';
import '../Policies.dart';
import '../Settings.dart';
import '../Styles.dart';
import 'GameOver.dart';
import 'dart:async';

class Board extends StatefulWidget {
  List<String> names;

  Board({this.names});

  @override
  State<StatefulWidget> createState() {
    return BoardState(names: names);
  }
}

class BoardState extends State<Board> {
  List<String> names;
  static var numPlayers;
  final fascistColor = Colors.deepOrange;
  final liberalColor = Colors.indigo;

  static var policy = new Policies();
  static var revealedPolicies = ["", "", ""];
  static var policyColors = [Colors.grey, Colors.grey, Colors.grey];
  var fasPolToWin = 6;
  var libPolToWin = 5;
  var selectRejectFlag = false;
  var fasPolInPlay = 0;
  var libPolInPlay = 0;
  static var invalidSelection;
  var buttonText = "Draw Policy";
  static var drawable = true;
  static var temp = true;

  static var settings = new Settings();

  static var _visible = false;

  BoardState({this.names});

  @override
  void initState() {
    super.initState();
    numPlayers = names.length;
    settings.setSettings(numPlayers, names);
    print("Settings Set!");
    Timer.run(() => revealAllRoles());
    // Have fascists see each other
  }

  @override
  Widget build(BuildContext context) {
    if (temp) {
      temp = false;
//      revealAllRoles();
    }

    return Scaffold(
        appBar: AppBar(
          title: Text(
            "Secret Hitler: $numPlayers Players",
            style: TextStyle(fontSize: 24),
          ),
          centerTitle: true,
          backgroundColor: SecretOrange, //Colors.deepOrange[800],
        ),
        backgroundColor: Background,
        body: Column(children: <Widget>[
          Spacer(flex: 1),
          Row(
              // GameBoard
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                getPolicyBoard(fascistColor, Colors.orange, 3, 3, fasPolInPlay),
                getPolicyBoard(
                    liberalColor, Colors.lightBlue, 1, 4, libPolInPlay),
              ]), // GameBoard
          Spacer(flex: 1),
          Row(
              // Policy Cards
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                getPolicyCard(revealedPolicies[0], policyColors[0], 0),
                getPolicyCard(revealedPolicies[1], policyColors[1], 1),
                getPolicyCard(revealedPolicies[2], policyColors[2], 2),
              ]), // Policy Cards
          Spacer(flex: 1),
          ButtonTheme(
              // Draw Policy
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
                  if (drawable) {
                    policy.drawPolicies();
                    revealedPolicies = policy.revealPolicies();
                    policyColors = policy.revealColors();
                    selectRejectFlag = true;
                    invalidSelection = 5;
                    drawable = false;
                    _visible = true;
                    setState(() {});
                  }
                },
              )),
          Spacer(flex: 1),
        ]));
  }

  Widget getPolicyBoard(var primaryColor, var secondaryColor, var numPrimary,
      var numSecondary, var polInPlay) {
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
              color: primaryColor,
              child: Padding(
                padding: EdgeInsets.all(15.0),
                child: Container(
                  color: Colors.yellowAccent,
                  child: Padding(
                    padding: EdgeInsets.all(3.0),
                    child: Column(children: policyTiles),
                  ),
                ),
              ),
            ),
          )),
    );
  }

  Widget getBoardTile(var color) {
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
        child:
            RotatedBox(quarterTurns: 3, child: getPolicyCard(text, color, 2)));
  }

  Widget getPolicyCard(String policyType, var policyColor, var number) {
    var validSelections = true;

    return AnimatedOpacity(
      opacity: _visible ? 1.0 : 0.0,
      duration: Duration(milliseconds: 500),
      child: InkWell(
          onTap: () {
            if (number != invalidSelection) {
              if (selectRejectFlag) {
                policyColors[number] = Colors.grey;
                revealedPolicies[number] = "X";
                selectRejectFlag = false;
                invalidSelection = number;
                _showDialog();
                setState(() {});
              } else {
                addPolicyToBoard(
                    policyColors[number], revealedPolicies[number]);
                selectRejectFlag = true;
                policyColors = [Colors.grey, Colors.grey, Colors.grey];
                revealedPolicies = ["X", "X", "X"];
                invalidSelection = 5;
                drawable = true;
                _visible = false;
                setState(() {});
              }
            }
          },
          child: Padding(
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
                                      ))))))))),
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
    if ((fasPolInPlay >= fasPolToWin) || (libPolInPlay >= libPolToWin)) {
      String winner;
      if (fasPolInPlay >= fasPolToWin) {
        winner = 'Fascists!';
      } else {
        winner = 'Liberals!';
      }
      Navigator.push(
          context,
          MaterialPageRoute(
              builder: (context) => new GameOver(winner: winner)));
    }
  }

  void _showDialog() {
    // flutter defined function
    showDialog(
      context: context,
      builder: (BuildContext context) {
        // return object of type Dialog
        return AlertDialog(
          title: new Text("Alert Dialog title"),
          content: new Text("Alert Dialog body"),
          actions: <Widget>[
            // usually buttons at the bottom of the dialog
            new FlatButton(
              child: new Text("Close"),
              onPressed: () {
                Navigator.of(context).pop();
//                setState(() {});
              },
            ),
          ],
        );
      },
    );
  }

  void revealAllRoles() {
    for (int i = names.length - 1; i >= 0; i--) {
      revealIndividualRole(i);

      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: new Text("Please pass to the following player: "),
            content: Text(settings.getPlayerName(i)),
            actions: <Widget>[
              new FlatButton(
                child: new Text("Close"),
                onPressed: () {
                  Navigator.of(context).pop();
//                setState(() {});
                },
              ),
            ],
          );
        },
      );
    }
  }

  void revealIndividualRole(int index) {
    var role = settings.getPlayerRole(index);
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: new Text(settings.getPlayerName(index)),
          content: new Text("You are playing as a $role"),
          actions: <Widget>[
            new FlatButton(
              child: new Text("Close"),
              onPressed: () {
                Navigator.of(context).pop();
//                setState(() {});
              },
            ),
          ],
        );
      },
    );
  }
}
