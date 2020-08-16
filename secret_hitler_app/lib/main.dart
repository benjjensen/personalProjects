/* TO DO:

  PHASE ONE: Local Play
      Aesthetics:
      - Flip boards to fill up, not down
      - Use flexible containers everywhere
      - Actually work on the aesthetics lol

      Logistics:
      - Disable card selection on redraw
      - Animations:
        - Drawing policies?
      - Presidential Actions

      - Making this multiple device (game code?)

      Other:
      - General code clean up


      Instructions: Add in a DefaultTabController for each page ?

  PHASE TWO: Online Play
   # Firebase
 */

import 'package:flutter/material.dart';
import 'dart:math';

import 'Pages/PlayerSetup.dart';
import 'Pages/Instructions.dart';

import 'Button.dart';
import 'Styles.dart';

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
          primaryColor: SecretPaleYellow, //Colors.yellow[100]),
        ),
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
      backgroundColor: SecretOrange, //Colors.deepOrange[800],
      body: Center(
        child: Column(
          // mainAxisAlignment, children
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
            Expanded(
              flex: 3,
              child: Transform.rotate(
                angle: -pi / 30,
                child: Center(
                  child: RichText(
                    text: TextSpan(
                        style: TextStyle(
                          fontFamily: "GermaniaOne",
                          fontSize: 72,
                          color: SecretPaleYellow, //Colors.yellow[100],
                          shadows: <Shadow>[
                            Shadow(
                              offset: Offset(3.0, 3.0),
                              blurRadius: 2.0,
                              color: Color.fromARGB(255, 0, 0, 0),
                            ),
                            Shadow(
                              offset: Offset(5.0, 4.0),
                              blurRadius: 2.0,
                              color: Color.fromARGB(255, 0, 0, 0),
                            ),
                            Shadow(
                              offset: Offset(7.0, 5.0),
                              blurRadius: 2.0,
                              color: Color.fromARGB(255, 0, 0, 0),
                            ),
                            Shadow(
                              offset: Offset(9.0, 6.0),
                              blurRadius: 2.0,
                              color: Color.fromARGB(255, 0, 0, 0),
                            ),
                            Shadow(
                              offset: Offset(11.0, 7.0),
                              blurRadius: 2.0,
                              color: Color.fromARGB(255, 0, 0, 0),
                            ),
                            Shadow(
                              offset: Offset(13.0, 8.0),
                              blurRadius: 2.0,
                              color: Color.fromARGB(255, 0, 0, 0),
                            ),
                            Shadow(
                              offset: Offset(15.0, 9.0),
                              blurRadius: 2.0,
                              color: Color.fromARGB(255, 0, 0, 0),
                            ),
                            Shadow(
                              offset: Offset(17.0, 10.0),
                              blurRadius: 2.0,
                              color: Color.fromARGB(255, 0, 0, 0),
                            ),
                            Shadow(
                              offset: Offset(19.0, 11.0),
                              blurRadius: 2.0,
                              color: Color.fromARGB(255, 0, 0, 0),
                            ),
                            Shadow(
                              offset: Offset(21.0, 12.0),
                              blurRadius: 2.0,
                              color: Color.fromARGB(255, 0, 0, 0),
                            ),
                            Shadow(
                              offset: Offset(23.0, 13.0),
                              blurRadius: 2.0,
                              color: Color.fromARGB(255, 0, 0, 0),
                            ),
                            Shadow(
                              offset: Offset(25.0, 14.0),
                              blurRadius: 2.0,
                              color: Color.fromARGB(255, 0, 0, 0),
                            ),
                            Shadow(
                              offset: Offset(29.0, 15.0),
                              blurRadius: 2.0,
                              color: Color.fromARGB(255, 0, 0, 0),
                            ),
                            Shadow(
                              offset: Offset(32.0, 16.0),
                              blurRadius: 2.0,
                              color: Color.fromARGB(255, 0, 0, 0),
                            ),
                          ],
                        ),
                        children: <TextSpan>[
                          TextSpan(text: "SECRET\n"),
                          TextSpan(text: "HITLER"),
                        ]),
                  ),
                ),
              ),
            ),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: getButton(context, "Instructions", () {
                  Navigator.push(context,
                      MaterialPageRoute(builder: (context) => Instructions()));
                }),
              ),
            ),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: getButton(context, "Begin Local Game", () {
                  Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (context) => new PlayerSetup()));
                }),
              ),
            ),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: getButton(context, "Begin Online Game", () {}),
              ),
            ),
            Container(
              height: 40,
            ),
          ],
        ),
      ),
    );
  }
}
