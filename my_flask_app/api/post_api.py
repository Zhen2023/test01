#api/post_api.py

from flask import jsonify,request,current_app,url_for
from . import api_bp
from ..models import Post

@api_bp.route('/posts',methods=['GET'])
def get_posts():
    #获取分页参数
    page = request.args.get('page',1,type=int)
    per_page = request.args.get('per_page',current_app.config.get('POSTS_PER_PAGE',10),type=int)

    pagination = Post.query.order_by(Post.create_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    posts_list = [post.to_dict() for post in pagination.items ]
    response = {
        'items': posts_list,
        '_meta': {
            'page': page,
            'per_page': per_page,
            'total_pages': pagination.pages,
            'total_items': pagination.total
        },
        '_links': {
            'self': url_for('api.get_posts', page=page, per_page=per_page, _external=True),
            'next': url_for('api.get_posts', page=pagination.next_num, per_page=per_page, _external=True) if pagination.has_next else None,
            'prev': url_for('api.get_posts', page=pagination.prev_num, per_page=per_page, _external=True) if pagination.has_prev else None
        }
    }

    return jsonify(response)
    