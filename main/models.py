from django.db import models

# Create your models here.
# 게시글(Post)엔 제목(postname), 내용(contents)이 존재합니다
class Post(models.Model):
    postname = models.CharField(max_length=50)
    contents = models.TextField()

    # 게시글의 제목(postname)이 Post object 대신하기
    def __str__(self):
        return self.postname

class Craw(models.Model):
    snum = models.AutoField(db_column='sNum', primary_key=True)  # Field name made lowercase.
    id = models.CharField(max_length=50)
    lname = models.CharField(db_column='lName', max_length=50)  # Field name made lowercase.
    title = models.TextField()
    degree = models.CharField(max_length=50)
    acheck = models.CharField(db_column='aCheck', max_length=50)  # Field name made lowercase.
    con = models.TextField()
    sdate = models.DateTimeField(db_column='sDate')  # Field name made lowercase.
    edate = models.DateTimeField(db_column='eDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'craw'