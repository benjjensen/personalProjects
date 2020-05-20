/* TO DO:
      Aesthetics:
      - Flip boards to fill up, not down
      - Use flexible containers everywhere
      - Actually work on the aesthetics lol

      Logistics:
      - Disable card selection on redraw
      - Allow multiple games to be played ('reset' option?)
      - Animations:
        - Drawing policies?

      - Making this multiple device (game code?)

      Other:
      - General code clean up
 */

import 'package:flutter/material.dart';
import 'dart:math';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        // Title, Theme, Home:
        theme: ThemeData(
//        primarySwatch: Colors.purple
            primaryColor: Colors.purple),
        home: MainPage());
  }
}

class MainPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // appBar
      appBar: AppBar(
        // Title,
        title: Text("Secret Hitler"),
        centerTitle: true,
      ),
      body: Center(
        child: Column(
          // mainAxisAlignment, children
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: <Widget>[
            getButton(context, "Instructions", () {
              Navigator.push(context,
                  MaterialPageRoute(builder: (context) => Instructions()));
            }),
            getButton(context, "New Game", () {
              Navigator.push(context,
                  MaterialPageRoute(builder: (context) => Page_PlayerSetup()));
            })
          ],
        ),
      ),
    );
  }
}

class Page_PlayerSetup extends StatefulWidget {
  /*  Player Setup
        Generates a form to gather the number of players and player names
   */

  @override
  _Page_PlayerSetupState createState() => _Page_PlayerSetupState();
}

class _Page_PlayerSetupState extends State<Page_PlayerSetup> {
  var minPlayers = 5;
  var maxPlayers = 10;
  var numPlayers = 5;

  final _formKey = GlobalKey<FormState>();

  List<String> names = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Player Setup", style: TextStyle(fontSize: 24)),
      ),
      body: Center(
        child: Padding(
          padding: EdgeInsets.all(15.0),
          child: Column(
            children: <Widget>[
              Text(
                "Player Names",
                style: TextStyle(fontSize: 20),
              ),
              Form(
                key: _formKey, // Used for the validation step
                child:
                    GetForm_playerNames(), // Returns a TextFormField with the appropriate number of name fields
              ),
              GetAddRemoveButtons(),
            ],
          ),
        ),
      ),
    );
  }

  Widget GetForm_playerNames() {
    var playerForm = List<Widget>();
    for (var player = 0; player < numPlayers; player++) {
      playerForm.add(TextFormField(
        decoration: const InputDecoration(
          hintText: 'Enter player name',
        ),
        validator: (String value) {
          if (value.isEmpty) {
            return 'Please input a name';
          }
          names.add(value);
          return null;
        },
      ));
    }
    return Column(children: playerForm);
  }

  Widget GetAddRemoveButtons() {
    var buttonList = List<Widget>();

    if (numPlayers < maxPlayers) {
      buttonList.add(BuildButton(context, "Add Player", () {
        numPlayers++;
        setState(() {});
      }));
    }
    if (numPlayers > minPlayers) {
      buttonList.add(BuildButton(context, "Remove Player", () {
        numPlayers--;
        setState(() {});
      }));
    }
    buttonList.add(BuildButton(context, "Begin", () {
      if (_formKey.currentState.validate()) {
        Navigator.push(context,
            MaterialPageRoute(builder: (context) => Board(names: names)));
        setState(() {});
      }
    }));
    return Center(
      child: Row(
        children: buttonList,
        mainAxisAlignment: MainAxisAlignment.center,
      ),
    );
  }

  Widget BuildButton(BuildContext context, String text, VoidCallback callback) {
    return Padding(
      padding: EdgeInsets.all(10.0),
      child: ButtonTheme(
        minWidth: 150,
        height: 50,
        child: RaisedButton(
          textColor: Colors.black,
          color: Colors.greenAccent,
          child: Text(text, style: TextStyle(fontSize: 18)),
          shape: RoundedRectangleBorder(
            side: BorderSide(
              color: Colors.blue,
              width: 1,
            ),
            borderRadius: BorderRadius.all(Radius.circular(30)),
          ),
          onPressed: callback,
        ),
      ),
    );
  }
}

class Page_GameOver extends StatelessWidget {
  String winner;

  Page_GameOver({this.winner});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          "Game Over",
          style: TextStyle(fontSize: 18),
        ),
      ),
      body: Center(
        child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: <Widget>[
              Text(
                "Game Over",
                style: TextStyle(fontSize: 36),
              ),
              Text(
                "Winner: $winner",
                style: TextStyle(fontSize: 36),
              ),
              getButton(context, 'Return to Main Menu', () {
                Navigator.push(context,
                    MaterialPageRoute(builder: (context) => MainPage()));
              })
            ]),
      ),
    );
  }
}

class Instructions extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // appBar, body
      appBar: AppBar(
          title: Text("Instructions", style: TextStyle(fontSize: 24)),
          backgroundColor: Colors.redAccent),
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
            ]),
      ),
    );
  }
}

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
  static var revealedPolicies = ["Void", "Void", "Void"];
  static var policyColors = [Colors.grey, Colors.grey, Colors.grey];
  var fasPolToWin = 6;
  var libPolToWin = 5;
  var selectRejectFlag = false;
  var fasPolInPlay = 0;
  var libPolInPlay = 0;
  static var invalidSelection;
  var buttonText = "Draw Policy";

  static var settings = new Settings();

  BoardState({this.names});

  @override
  Widget build(BuildContext context) {
    if (!(settings.isSetup())) {
      // Probably a better way to do this, but...
      numPlayers = names.length;
      settings.setSettings(numPlayers, names);
      print("Settings Set!");
    }

    return Scaffold(
        appBar: AppBar(
          title: Text(
            "Secret Hitler: $numPlayers Players",
            style: TextStyle(fontSize: 24),
          ),
          centerTitle: true,
        ),
        backgroundColor: Colors.blueGrey,
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
                  policy.drawPolicies();
                  revealedPolicies = policy.revealPolicies();
                  policyColors = policy.revealColors();
                  selectRejectFlag = true;
                  invalidSelection = 5;
                  setState(() {});
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
              color: primaryColor, //Colors.deepOrange,
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

    return InkWell(
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
                                    )))))))));
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
      if (fasPolInPlay > fasPolToWin) {
        winner = 'Fascists!';
      } else {
        winner = 'Liberals!';
      }
      Navigator.push(
          context,
          MaterialPageRoute(
              builder: (context) => Page_GameOver(winner: winner)));
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
      child: Text(text, style: TextStyle(fontSize: 24)),
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

class Settings {
  static var numPlayers;
  static List<String> playerNames;
  static List<String> roles = [];

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

    for (var i = 0; i < numPlayers; i++) {
      String playerName = playerNames[i];
      String role = roles[i];
      print("$playerName: $role\n");
    }
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
}
