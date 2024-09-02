from datacenter.models import Schoolkid, Mark, Subject
from datacenter.models import Chastisement
from datacenter.models import Commendation
from datacenter.models import Lesson
import random

texts=["Молодец!", "Отлично!", "Хорошо!", "Гораздо лучше, чем я ожидал!", "Ты меня приятно удивил!", "Великолепно!", "Прекрасно!", "Ты меня очень обрадовал!", "Именно этого я давно ждал от тебя!", "Сказано здорово – просто и ясно!", "Ты, как всегда, точен!", "Очень хороший ответ!", "Талантливо!", "Ты сегодня прыгнул выше головы!", "Я поражен!", "Уже существенно лучше!", "Потрясающе!", "Замечательно!", "Прекрасное начало!", "Так держать!", "Ты на верном пути!", "Здорово!", "Это как раз то, что нужно!", "Я тобой горжусь!", "С каждым разом у тебя получается всё лучше!", "Мы с тобой не зря поработали!", "Я вижу, как ты стараешься!", "Ты растешь над собой!", "Ты многое сделал, я это вижу!", "Теперь у тебя точно все получится!"]

def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lte='3')
    for bad_mark in bad_marks:
        bad_mark.points=5
        bad_mark.save()
def del_chastisement(schoolkid):
    child_chastisement = Chastisement.objects.filter(schoolkid=schoolkid)
    child_chastisement.delete()

def create_commendation(schoolkid, subject): 

    lessons = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter, subject__title=subject)
    lesson = random.choice(lessons.order_by('date'))
    text = random.choice(texts)
    Commendation.objects.create(teacher=lesson.teacher, subject=lesson.subject, created=lesson.date, schoolkid=schoolkid, text=text)

def main(pupil_name, subject):
    schoolkid = Schoolkid.objects.get(full_name__contains=pupil_name)
    fix_marks(schoolkid)
    del_chastisement(schoolkid)
    create_commendation(schoolkid, subject)
