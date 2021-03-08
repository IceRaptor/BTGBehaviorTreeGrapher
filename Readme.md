# BTGBehaviorTreeGrapher

Generates a PDF graph of the behavior tree that the AI units in BTG use.

Usage: 
* Decompile the `BehaviorTree.InitRootFunction` in AssemblyCSharp.dll
* Decompile each listed tree. Copy the instructions inside the `InitRootNode` method of the behavior tree into a file. 
* Run this utility against the file: `main.py -i <INPUT_FILE>`
* Run blockdiag.com/en/index.html against the output diag file: `blockdiag -Tpdf <INPUT_FILE>.diag`
