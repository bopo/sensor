//index.js
//获取应用实例
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
    var l_user = _this.data.user,  //本页用户数据
        g_user = app._user; //全局用户数据
    //排除第一次加载页面的情况（全局用户数据未加载完整 或 本页用户数据与全局用户数据相等）
    if(isEmptyObject(l_user) || !g_user.openid || isEqualObject(l_user.we, g_user.we)){
      return false;
    }
    //全局用户数据和本页用户数据不一致时，重新获取卡片数据
    if(!isEqualObject(l_user.we, g_user.we)){
      //判断绑定状态
      if(!g_user.is_bind){
        _this.setData({
          'remind': '未绑定'
        });
      }else{
        _this.setData({
          'remind': '加载中'
        });
        //清空数据
        _this.setData({
          user: app._user
        });
        _this.getItemData();
      }
    }
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
    //然后再尝试登录用户, 如果缓存更新将执行该回调函数
    app.getUser(function(status){
      _this.response.call(_this, status);
    });
  },
  response: function(status){
    var _this = this;
    if(status){
      if(status != '离线缓存模式'){
        //错误
        _this.setData({
          'remind': status
        });
        return;
      }else{
        //离线缓存模式
        _this.setData({
          offline: true
        });
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
        console.log(res)
      }
    });
  },
  getItemData: function(){
    var _this = this;
    //判断并读取缓存
    wx.showNavigationBarLoading();
  }
});
