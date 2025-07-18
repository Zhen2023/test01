#blog/routes.py

from flask import render_template, request, redirect, url_for,flash,current_app,jsonify,abort
from . import blog_bp
from my_flask_app.extensions import db
from flask_login import login_required,current_user
from my_flask_app.models import Post,Tag,Comment
from .forms import PostForm,CommentForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_


@blog_bp.route('/posts')
def posts():
    return render_template('blog/posts.html', title='文章列表')
    # page = request.args.get('page', 1, type=int)
    # per_page = current_app.config.get('POSTS_PER_PAGE', 10)
    # pagination = Post.query.order_by(Post.create_time.desc()).paginate(
    #     page=page,per_page=per_page,error_out=False
    # )
    # posts_on_page = pagination.items
    # return render_template('blog/posts.html',posts=posts_on_page,pagination=pagination,title = '文章列表')


@blog_bp.route('/new_post',methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data 
        summary = content[:200]
        tags_string = form.tags_string.data
        tags = []
        if tags_string:
            tags_list =[tag_name.strip() for tag_name in tags_string.split(",") if tag_name.strip()]
            for name in tags_list:
                tag = Tag.query.filter_by(name=name).first()
                if tag:
                    tags.append(tag)
                else:
                    new_tag =Tag(name=name)
                    db.session.add(new_tag)
                    tags.append(new_tag)

        post = Post(title=title,content=content,author=current_user,summary=summary,tags=tags)
   

        try:
            db.session.add(post)
            db.session.commit()
            flash("文章已成功保存","success")
        except Exception as e:
            db.session.rollback()
            flash(f"文章保存失败：{e}","danger")
            print(f"文章保存，发生未知异常：{e}")
        return redirect(url_for('blog.posts')) #这里是指发布成功后回到文章列表页面，对吧
  
    return render_template('blog/new_or_edit_post.html',form=form,title = '发布新文章',legend='发布新文章')

@blog_bp.route('/post_detail/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    comments = post.comments.order_by(Comment.create_time.desc()).all()
    return render_template('blog/post_detail.html',post=post,title = post.title,form=form,comments=comments)

@blog_bp.route('/edit_post/<int:post_id>',methods=['GET','POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        flash("您没有权限编辑此文章","danger")
        return redirect(url_for('blog.post_detail',post_id=post.id))
    
    if request.method == 'GET':
        form = PostForm(obj=post)
        form.tags_string.data = ",".join([tag.name for tag in post.tags])
    else:
        form = PostForm()# 创建一个空表单来接收提交的数据

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.summary = form.content.data[:200]
        tags_string = form.tags_string.data
        tags=[]
        if tags_string:
            tags_list = [tag_name.strip() for tag_name in tags_string.split(",") if tag_name.strip()]
            for name in tags_list:
                tag = Tag.query.filter_by(name=name).first()
                if not tag:
                    tag =Tag(name=name)
                    db.session.add(tag)
                tags.append(tag)
        post.tags = tags          
        try:
            db.session.commit()
            flash("文章已成功更新","success")
        except Exception as e:
            db.session.rollback()
            flash(f"文章更新失败：{e}","danger")
            print(f"文章更新时发生未知异常：{e}")
        return redirect(url_for('blog.post_detail',post_id=post.id))
    return render_template('blog/new_or_edit_post.html',form=form,post=post,title = '编辑文章',legend=f"编辑:{post.title}",post_id=post.id)
        
@blog_bp.route('/delete_post/<int:post_id>',methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash("您没有权限删除此文章","danger")
        return redirect(url_for('blog.post_detail',post_id=post.id))
    try:
        db.session.delete(post)
        db.session.commit()
        flash("文章已成功删除","success")
    except Exception as e:
        db.session.rollback()
        flash(f"文章删除失败：{e}","danger")
        print(f"文章删除时发生未知异常：{e}")
    return redirect(url_for('blog.posts'))

@blog_bp.route('/search')
def search():
    query_string = request.args.get('q','')
    if not query_string:
        flash("请输入搜索关键词","warning")
        return redirect(url_for('blog.posts'))
    page = request.args.get('page',1,type=int)
    per_page = current_app.config.get('POSTS_PER_PAGE',10)
    search_results = Post.query.filter(
        or_(
            Post.title.like(f'%{query_string}%'),
            Post.content.like(f'%{query_string}%')
        )
    ).order_by(Post.create_time.desc())

    #分页
    pagination = search_results.paginate(
        page=page,per_page=per_page,error_out = False
    )
    posts_on_page = pagination.items #返回当前页供展示
    flash(f"共找到{pagination.total}条关于{query_string}的文章","success")
    return render_template('blog/posts.html',posts=posts_on_page,pagination=pagination,title=f"搜索结果：{query_string}",search_query=query_string)

@blog_bp.route('/post/<int:post_id>/like',methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.likes is None:
        post.likes = 0
    
    post.likes += 1

    try:
        db.session.commit()
        return jsonify({'status':'success','likes':post.likes})
    except Exception as e:
        db.session.rollback()
            # 如果出错，返回一个包含错误信息的 JSON，并设置 HTTP 状态码为 500
        current_app.logger.error(f"Error liking post {post_id}: {e}")
        return jsonify({'status': 'error', 'message': '数据库更新失败'}), 500
        
@blog_bp.route('/post/<int:post_id>/unlike',methods=['POST'])
@login_required
def unlike_post():
    pass

@blog_bp.route('/post/<int:post_id>/add_comment',methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)

    form = CommentForm()
    if form.validate_on_submit():
        content = form.content.data 
        comment = Comment(content=content,post=post,author=current_user)
        try:

            db.session.add(comment)
            db.session.commit()
            flash("评论发布成功","success")
            print("评论发布成功")

        except Exception as e:
            db.session.rollback()
            flash("评论发表失败","danger")
            current_app.logger.error(f"Error adding comment for post {post_id}: {e}")
    else:
        for field,errors in form.errors.items():
            for error in errors:
                flash(f"发表评论失败：{getattr(form,field).label.text + error}","danger")
    
    return redirect(url_for('blog.post_detail',post_id=post.id))


@blog_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    # 1. 根据 ID 查询要删除的评论，如果不存在则 404
    comment_to_delete = Comment.query.get_or_404(comment_id)
    
    # 为了重定向，我们需要知道这条评论属于哪篇文章
    post_id = comment_to_delete.post.id

    # 2. 权限检查：
    #    - 当前登录用户必须是评论的作者
    #    - 或者，当前登录用户是这篇文章的作者
    if current_user != comment_to_delete.author and current_user != comment_to_delete.post.author:
        # 如果两个条件都不满足，就中止操作并返回 403 Forbidden 错误
        from flask import abort
        abort(403) # 403 表示禁止访问

    # 3. 执行删除操作
    try:
        db.session.delete(comment_to_delete)
        db.session.commit()
        flash('评论已成功删除。', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'删除评论时发生错误: {e}', 'danger')
        current_app.logger.error(f"Error deleting comment {comment_id}: {e}")

    # 4. 重定向回文章详情页
    return redirect(url_for('blog.post_detail', post_id=post_id))