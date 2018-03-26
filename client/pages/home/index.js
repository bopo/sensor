// 获取应用实例
var app = getApp();

Page({
  data: {
    offline: false,
    remind: '加载中',
    user: {},
    disabledItemTap: false //点击了不可用的页面
  },
  //分享
  onShareAppMessage: function(){
    return {
      title: '星迹美晒',
      desc: '星迹美晒',
      path: '/pages/home/index'
    };
  },
  //下拉更新
  onPullDownRefresh: function(){
    if(app._user.is_bind){
      this.getItemData();
    }else{
      wx.stopPullDownRefresh();
    }
  },
  onShow: function(){
    var _this = this;
    //离线模式重新登录
    if(_this.data.offline){
      _this.login();
      return false;
    }
    function isEmptyObject(obj){ for(var key in obj){return false;} return true; }
    function isEqualObject(obj1, obj2){ if(JSON.stringify(obj1) != JSON.stringify(obj2)){return false;} return true; }
  },
  onLoad: function(){
    this.login();
  },
  login: function(){
    var _this = this;
    //如果有缓存，则提前加载缓存
    if(app.cache.version === app.version){
      try{
        _this.response();
      }catch(e){
        //报错则清除缓存
        app.cache = {};
        wx.clearStorage();
      }
    }
  },
  response: function(status){
    var _this = this;
    if(status){
      if(status != '离线缓存模式'){
        return _this.setData({'remind': status });
      }else{
        _this.setData({offline: true });
      }
    }
    _this.setData({
      user: app._user
    });
    //判断绑定状态
    if(!app._user.is_bind){
      _this.setData({
        'remind': '未绑定'
      });
    }else{
      _this.setData({
        'remind': '加载中'
      });
      _this.getItemData();
    }
  },
  disabled_item: function(){
    var _this = this;
    if(!_this.data.disabledItemTap){
      _this.setData({
        disabledItemTap: true
      });
      setTimeout(function(){
        _this.setData({
          disabledItemTap: false
        });
      }, 2000);
    }
  },
  scanQR: function() {
    wx.scanCode({
      onlyFromCamera: true,
      scanType: 'qrCode',
      success: (res) => {
        console.log(res);
      }
    });
  },
  getItemData: function(){
    var _this = this;
    wx.showNavigationBarLoading();
  }
});
