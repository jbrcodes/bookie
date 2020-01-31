# app/models.py

from sqlalchemy import func

from app import db



class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    
    
    # -----------------------------------------------------
    
    
    @classmethod
    def Get(cls, id):
        return cls.query.get(id)
    
    
    @classmethod
    def GetAll(cls):
        """ Return a list of all tags """
        return Tag.query.order_by(Tag.name).all()
    
    
    @classmethod
    def Delete(cls, t):
        db.session.delete(t)
        db.session.commit()
            
            
    @classmethod
    def NamesToTags(cls, nameList):
        """
        Converts a name list to a tag list.
        Creates any tags that don't already exist.
        """
        tagList = []
        for name in nameList:
            t = Tag.query.filter_by(name=name).first()
            if not t:
                t = Tag(name)
                db.session.add(t)
            tagList.append(t)

        return tagList
    
    
    @classmethod
    def TagsToNames(cls, tagList):
        """ Convert a tag list to a name list """
        nameList = [ t.name for t in tagList ]
        nameList.sort()

        return nameList
            

    # -----------------------------------------------------

    
    def __init__(self, name):
        self.name = name
        
        
    def __repr__(self):
        return '<Tag ({}) ({})>'.format(self.id, self.name)


    def _jsonify(self):
        return self.name