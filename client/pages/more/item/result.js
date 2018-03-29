// 获取应用实例
var app = getApp();

Page({
  data: {
    version: ''
  },
  onLoad: function(){
    this.setData({
      version: app.version
    });
  }
});
