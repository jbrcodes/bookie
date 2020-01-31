# app/mods/bookmark/models.py

from datetime import datetime

from app import db
from app.models import Tag



bookmarksTags = db.Table('bookmarks_tags',
    db.Column('bookmarkId', db.Integer, db.ForeignKey('bookmarks.id')),
    db.Column('tagId', db.Integer, db.ForeignKey('tags.id'))
)

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    title = db.Column(db.String())
    note = db.Column(db.String())
    visitCount = db.Column(db.Integer(), default=0)
    lastVisitStamp = db.Column(db.DateTime())
    
    tags = db.relationship('Tag', 
        order_by=Tag.name,
        secondary=bookmarksTags)

    # ------------------------------------

    @classmethod
    def Get(cls, id):
        return Bookmark.query.get(id)
    
    @classmethod
    def Delete(cls, bm):
        db.session.delete(bm)
        db.session.commit()
    
    @classmethod
    def Select(cls, **kwargs):
        # What are we querying?
        if 'tag' in kwargs:
            # Use ilike() for case-insensitive search
            criterion = Bookmark.tags.any(Tag.name.ilike(kwargs['tag']))
            result = Bookmark.query.filter(criterion)
        elif 'popular' in kwargs:
            result = db.session.query(Bookmark)\
                .order_by(Bookmark.visitCount.desc(), Bookmark.title)
        else:
            result = db.session.query(Bookmark)
            
        # Limit?
        if 'limit' in kwargs:
            result = result.limit(kwargs['limit'])
        
        if result:
            bmList = result.all()
        else:
            bmList = []
            
        return bmList
            
        
    @classmethod
    def FindAllTags(cls):
        """ Return a list of used tags """
        tagList = db.session.query(Tag).outerjoin(bookmarksTags)\
            .filter(bookmarksTags.c.bookmarkId != None)\
            .order_by(Tag.name.desc())\
            .all()
        
        return tagList
    
    

    """
    
    # The following may be useful one day
        
    @classmethod
    def GetAllCounts(cls):
        " Return a dict of all tags and their use counts ""
        result = db.session.query(Tag, func.count(bookmarksTags.c.bookmarkId))\
            .join(bookmarksTags)\
            .group_by(Tag)\
            .order_by(Tag.name)
        # Convert Tag objs to names
        nameList = [ (rec[0].name, rec[1]) for rec in result ]
        # Convert to dict with name => count
        nameDict = dict(nameList)
        
        return nameDict

    """
    
    # -----------------------------------------------------
        
        
    def __init__(self, url, title, **kwargs):
        super(Bookmark, self).__init__(**kwargs);
        self.url = url
        self.title = title
        
        
    def __repr__(self):
        return '<Bookmark ({}) ({})>'.format(self.id, self.title)


    def bumpVisitCount(self):
        self.visitCount += 1
        self.lastVisitStamp = datetime.now()
        db.session.commit()
        
        return self.visitCount

    
    """
    def _jsonify(self):
        b = self.__dict__
        del b['id']
        del b['_sa_instance_state']
        b['lastVisitStamp'] = util.formatStamp( b['lastVisitStamp'] )  # hack?

        return b
    """