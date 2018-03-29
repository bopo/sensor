// 获取应用实例
var app = getApp();

Page({
  data: {
    user: {}
  },
  onShow: function(){
    this.getData();
  },
  getData: function(){
    var _this = this;
    wx.getUserInfo({
      success: function(res) {
        var _user = res.userInfo;
        _user.balance = '0.00';
        _user.spending = '0.00';
        _user.telphone = '185002154896';
        _this.setData({
          'user': _user,
          'info': res.userInfo
        });
      }
    });
  }
});
