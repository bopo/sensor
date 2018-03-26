//more.js
//获取应用实例
var app = getApp();

Page({
  data: {
    user: {}
  },
  onShow: function(){
    this.getData();
  },
  getData: function(){
    this.setData({
      'user': app._user,
      'time': {
        'term': app._time.term,
        'week': app._time.week,
        'day': days[app._time.day - 1]
      },
      'bind': true
    });
  }
});
