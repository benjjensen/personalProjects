import 'package:flutter/material.dart';
import 'Styles.dart';

Widget getButton(BuildContext context, String text, VoidCallback callback) {
  return ButtonTheme(
    minWidth: 300,
    height: 80,
    child: RaisedButton(
      textColor: SecretPaleYellow, //Colors.yellow[100],
      color: Background, //Colors.blueGrey[800],
      child: Text(
        text,
        style: TextStyle(
          fontSize: 24,
        ),
      ),
      shape: RoundedRectangleBorder(
        side: BorderSide(
          color: SecretPaleYellow, //Colors.yellow[300],
          width: 1,
        ),
        borderRadius: BorderRadius.all(Radius.circular(30)),
      ),
      onPressed: callback,
    ),
  );
}
