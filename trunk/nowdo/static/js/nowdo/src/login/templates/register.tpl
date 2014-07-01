<form role="form" id="register-modal-form" action="/account/ajax_register" method="post">
    <div class="form-group ">
        <span class="text-danger">

        </span>
        <a class="pull-right change-status" href="javascript: void(0);"  data-target_status="login">立即登录</a>
        <input class="form-control input-lg" id="email" name="email" placeholder="邮箱" type="text" value="">
    </div>
    <div class="form-group ">
        <input class="form-control input-lg" id="password" name="password" placeholder="账号密码" type="password" value="">
    </div>
    <div class="form-group">
        <input class="form-control input-lg" id="nickname" name="nickname" placeholder="昵称" type="text" value="">
    </div>
    <div class="form-group">
        <button class="btn btn-success btn-block btn-lg" type="submit">注册</button>
    </div>
    <div class="form-group">
        <input type="checkbox" id="agreement">
        <label class="control-label" for="agreement">我已经认真阅读并同意脑洞的《<a class="" href="/index" target="_blank">使用协议</a>》。
        </label>
    </div>
</form>