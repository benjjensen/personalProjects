import 'package:flutter/material.dart';
import '../Button.dart';
import '../Styles.dart';

class Instructions extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // appBar, body
      backgroundColor: Background,
      appBar: AppBar(
        title: Text("Instructions", style: TextStyle(fontSize: 24)),
        backgroundColor: SecretOrange, //Colors.deepOrange[800],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: <Widget>[
            Center(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Text(
                  "Gameplay",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 30,
                  ),
                ),
              ),
            ),
            Expanded(
              flex: 4,
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: ListView(
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Text(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque tristique hendrerit quam vel faucibus. Praesent facilisis sit amet est ut suscipit. Etiam pretium, quam non rutrum venenatis, lorem libero tincidunt nulla, ut maximus libero lacus a erat. Sed elit massa, maximus vitae velit a, mollis pharetra tellus. Vivamus blandit vehicula risus et laoreet. Maecenas cursus libero mattis tempus interdum. Donec suscipit purus a mi aliquam, eget pulvinar mi tempus. Morbi ut pretium elit, et tempor neque. Aliquam vel congue ex. Cras aliquet metus fringilla nisi placerat mollis. \nDonec lorem eros, auctor sed vestibulum quis, porttitor tempus tortor. Donec in neque pulvinar, porta nunc non, porta tortor. Nunc sit amet enim tellus. Donec vulputate vestibulum justo, a hendrerit eros. Praesent nec est et diam tristique pretium. Donec tellus libero, interdum laoreet turpis a, volutpat sodales urna. Ut laoreet lacus id ipsum varius, at facilisis tellus gravida. Nam quis vestibulum mi. Pellentesque vitae lectus facilisis mi ornare hendrerit at at lacus. Phasellus sit amet consectetur tortor. Pellentesque et fermentum lorem. Nullam tristique volutpat aliquet. Maecenas elementum lacus metus, in sodales dui euismod nec. Cras sodales leo vulputate massa lobortis rutrum. Nunc elementum in leo vel gravida. Curabitur rutrum a leo at congue.",
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 18,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: getButton(context, "Return to Main Menu", () {
                Navigator.pop(context);
              }),
            ),
          ],
        ),
      ),
    );
  }
}
