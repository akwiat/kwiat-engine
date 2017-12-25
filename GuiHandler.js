function SpecificGuiHandler() {
  this.guiobj = {
      Energy:SharedData.PlayerMaxLife
      ,Speed:0
      ,Base:SharedData.BaseLife

    };
  this.gui = new dat.GUI();
  this.energy = this.gui.add(this.guiobj,"Energy").min(0).max(SharedData.PlayerMaxLife).step(.001);
  this.base = this.gui.add(this.guiobj,"Base").min(0).max(SharedData.BaseLife).step(.001);
  this.speed = this.gui.add(this.guiobj,"Speed").min(0).max(SharedData.PlayerMaxSpeed).step(.001);

}
SpecificGuiHandler.prototype.setAndUpdate = function(str,obj,val) {
  this.guiobj[str] = val;
  this[obj].updateDisplay();
}
SpecificGuiHandler.prototype.update = function() {
  if (clientgame.player) {
  var realenergy = client.player.life;
  if (realenergy != this.guiobj.Energy) {
    this.guiobj.Energy = realenergy;
    this.energy.updateDisplay();
  }
  }
}

class GuiHandler() {
  constructor() {
    this.guiobj = {};
    this.gui = new dat.GUI();
  }
  // To update the gui, just change the values in the object..
  // To have changes to the gui do stuff, use the callback
}