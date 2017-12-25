//define( ["util/AlexUtils"], function (util) {
var util = require("util/AlexUtils");
require("style-loader!css-loader!lib/jquery.terminal-0.10.12.css");
require("script!lib/jQuery.js");

require("script!lib/jquery.terminal.js")
var Terminal = function(divName) {
  this.terminal = undefined;
  this.divName = divName;
  this.controlFn = Terminal.basicControlFn.bind(this);


  this.rootObj = new util.TrackedObj();
  this.currentObj = this.rootObj;

  this.currentpath = "";
}
Terminal.prototype.setPrompt = function() {
  this.terminal.set_prompt(this.currentpath + "> ");
  //debugger;
}
Terminal.prototype.selectSpecificObject = function (obj, path) {
  this.currentObj = obj;
  this.currentpath = path;
  this.setPrompt();
  if (this.currentObj === undefined) throw new Error("bad selectObject");
}
Terminal.prototype.selectObject = function(str) {
  if (str) {
	  this.currentObj = this.currentObj[str];
    this.currentpath += ("/" + str);
    this.setPrompt();
    //this.terminal.set_prompt(this.currentpath + "> ");
  }
  else {
    this.currentObj = this.rootObj;
    this.currentpath = "root";
    this.setPrompt();
    //this.terminal.set_prompt(this.currentpath+"> ");
  }

	if (this.currentObj === undefined) throw new Error("bad selectObject");
  //this.terminal.set_prompt(str+"> ");
  //this.terminal.echo("select object: "+str);
	//debugger;
}
//Terminal.prototype.
Terminal.prototype.echo = function(str) {
	this.terminal.echo(str);
}
Terminal.checkTerminalCommands = function(term, command, arr) {
  if (command == "cd") {
    if (arr.length != 1) term.echo("change object needs 1 arg");
    if (this.currentObj[ arr[0] ]) {
      this.selectObject(arr[0]);
      return true;
    } else {
      if (this.currentObj.hasOwnProperty(arr[0]))
        {term.echo("that object is undefined.."); return true; }
      else
        term.echo("cd bad arg: "+arr[0]);
    }
  } else if (command == "root") {
    this.selectObject(undefined);
    return true;
  } else if (command == "ls") {
    var str = "";
    for (var i in this.currentObj) {
      if (this.currentObj.hasOwnProperty(i))
        str += i;
        str += "\n";
     }
     this.echo(str);
     return true;
  } else if (command == "debugger") {
    debugger;
  }
}
Terminal.basicControlFn = function(command, term) {
	if (command !== '') {
		//debugger;
		var arr = command.split(' ');
		var removed = arr.splice(0,1);
		var name = removed[0];
		var n = this.currentObj[name];
    //if (n)
    var termCommandRet = Terminal.checkTerminalCommands.call(this, term, name, arr);
		if (termCommandRet) return;
    if (!n) {
			term.echo ("bad command: "+command);
			//debugger;
		}
		else if (typeof n == "function") {
			var obj = n.apply(this.currentObj, arr);
			if (obj)
				term.echo(obj);
    } else if (arr[0] == "=") {
      if (arr[1] === undefined) throw new Error("missing arg in assign");
      var ans;
      var p = parseFloat(arr[1]);
      if (p != NaN) ans = p; 
      else ans = arr[1];
      this.currentObj[name] = ans;
    }
    else {
           term.echo('');
    }
    
}
}
var TerminalManager = function() {
  this.terminals = new util.TrackedObj();
  this.firstTerminal = undefined;
}
TerminalManager.prototype.echo = function(msg) {
  if (this.firstTerminal) this.firstTerminal.echo(msg);
}
TerminalManager.prototype.selectObject = function(obj) {
  if (this.firstTerminal) this.firstTerminal.selectObject(obj);
}
TerminalManager.prototype.selectSpecificObject = function(obj, path) {
  if (this.firstTerminal) this.firstTerminal.selectSpecificObject(obj, path);
}
TerminalManager.prototype.initialize = function(onComplete) {
  //debugger;
  jQuery(function(dollarsign, undefined){
    //debugger;
     this.registerTerminals(dollarsign);
     onComplete.call(this);
     //this.afterTerminalSetup();
  }.bind(this));
}
TerminalManager.prototype.addTerminal = function(divName) {
  var nt = new Terminal(divName);
  this.terminals.register(divName, nt);
  if (!this.firstTerminal) this.firstTerminal = nt;
  return nt;

}
TerminalManager.prototype.getTerminal = function(name) {
	return this.terminals[name];
}
TerminalManager.prototype.registerTerminals = function(dollarsign) {
	this.terminals.forEach(this.registerOneTerminal.bind(this,dollarsign));
}
TerminalManager.prototype.registerOneTerminal = function(dollarsign, terminal) {
	var settingsObj = {
		greetings: 'Javascript Interpreter',
        name: 'js_demo',
        //height: 200,
        prompt: 'js> ',
        onInit: function(terminal) {
        	this.terminal = terminal;
        	//debugger;
        }.bind(terminal)
	}
	//debugger;
	var ret1 = dollarsign('#'+terminal.divName);
	ret1.terminal(terminal.controlFn, settingsObj);
	//debugger;
	/*
    dollarsign('#'+terminal.divName).terminal(function(command, term) {
        if (command !== '') {
            try {
                var result = window.eval(command);
                if (result !== undefined) {
                    term.echo(new String(result));
                }
            } catch(e) {
                term.error(new String(e));
            }
        } else {
           term.echo('');
        }
    }, {
        greetings: 'Javascript Interpreter',
        name: 'js_demo',
        height: 200,
        prompt: 'js> '
    });
*/
}

module.exports = TerminalManager;
//});
