import 'package:flutter/material.dart';
import '../Button.dart';
import '../main.dart';
import '../Styles.dart';

class GameOver extends StatelessWidget {
  String winner;

  GameOver({this.winner});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blueGrey[800],
      appBar: AppBar(
        title: Text(
          "Game Over",
          style: TextStyle(
            fontSize: 18,
            color: SecretPaleYellow,
          ),
        ),
        backgroundColor: SecretOrange, //Colors.deepOrange[800],
      ),
      body: Center(
        child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: <Widget>[
              Text(
                "Game Over",
                style: TextStyle(
                  fontSize: 36,
                  color: SecretPaleYellow,
                ),
              ),
              Text(
                "Winner: $winner",
                style: TextStyle(
                  fontSize: 36,
                  color: SecretPaleYellow,
                ),
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
