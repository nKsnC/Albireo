"""add cover_color an thumbnail_color to bangumi and episodes table

Revision ID: 3ffc63f8e34f
Revises: 44401c981696
Create Date: 2017-05-28 09:48:10.337370

"""

# revision identifiers, used by Alembic.
revision = '3ffc63f8e34f'
down_revision = '44401c981696'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import yaml
import os
from urlparse import urlparse
from utils.color import get_dominant_color


def get_base_path():
    fr = open('./config/config.yml', 'r')
    config = yaml.load(fr)
    return config['download']['location']


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bangumi', sa.Column('cover_color', sa.String(), nullable=True))
    op.add_column('episodes', sa.Column('thumbnail_color', sa.String(), nullable=True))
    # ### end Alembic commands ###
    connection = op.get_bind()
    result = connection.execute(sa.text('SELECT bangumi.id, bangumi.image FROM bangumi WHERE bangumi.image NOTNULL'))

    for row in result:
        bangumi_id = row[0]
        bangumi_image = row[1]
        base_path = get_base_path()
        path = urlparse(bangumi_image).path
        extname = os.path.splitext(path)[1]
        bangumi_path = base_path + '/' + str(bangumi_id)
        cover_path = bangumi_path + '/cover' + extname
        if not os.path.exists(bangumi_path):
            print 'cover not found for {0}'.format(bangumi_id)
            continue
        try:
            cover_color = get_dominant_color(cover_path, quality=5)
            connection.execute(sa.text(
                "UPDATE bangumi SET cover_color = '{0}' WHERE id = '{1}'".format(cover_color, bangumi_id)))
        except Exception as error:
            print error

        # query episodes
        episode_result = connection.execute(sa.text(
            "SELECT e.id, e.episode_no FROM episodes e WHERE e.status = 2 AND e.bangumi_id = '{0}'".format(bangumi_id)))
        for eps in episode_result:
            episode_id = eps[0]
            episode_no = eps[1]
            thumbnail_path = u'{0}/thumbnails/{1}.png'.format(bangumi_path, episode_no)
            if not os.path.exists(thumbnail_path):
                print 'thumbnail not found for {0}'.format(episode_id)
                continue
            try:
                thumbnail_color = get_dominant_color(thumbnail_path, quality=5)
                connection.execute(sa.text(
                    "UPDATE episodes SET thumbnail_color = '{0}' WHERE id = '{1}'".format(thumbnail_color, episode_id)))
            except Exception as error:
                print error

        print 'Finish for bangumi #{0}'.format(bangumi_id)

    print 'All done'


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('episodes', 'thumbnail_color')
    op.drop_column('bangumi', 'cover_color')
    # ### end Alembic commands ###
