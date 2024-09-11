from datacenter.models import Schoolkid, Mark
from datacenter.models import Chastisement
from datacenter.models import Commendation
from datacenter.models import Lesson
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import random
import argparse


praises=["Молодец!", "Отлично!", "Хорошо!", "Гораздо лучше, чем я ожидал!", "Ты меня приятно удивил!", "Великолепно!", "Прекрасно!", "Ты меня очень обрадовал!", "Именно этого я давно ждал от тебя!", "Сказано здорово – просто и ясно!", "Ты, как всегда, точен!", "Очень хороший ответ!", "Талантливо!", "Ты сегодня прыгнул выше головы!", "Я поражен!", "Уже существенно лучше!", "Потрясающе!", "Замечательно!", "Прекрасное начало!", "Так держать!", "Ты на верном пути!", "Здорово!", "Это как раз то, что нужно!", "Я тобой горжусь!", "С каждым разом у тебя получается всё лучше!", "Мы с тобой не зря поработали!", "Я вижу, как ты стараешься!", "Ты растешь над собой!", "Ты многое сделал, я это вижу!", "Теперь у тебя точно все получится!"]


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__lte='3').update(points=5)


def del_chastisement(schoolkid):
    child_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    child_chastisements.delete()


def create_commendation(schoolkid, subject): 
    lessons = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter, subject__title=subject)
    lesson = lessons.order_by('date').last()
    praise = random.choice(praises)
    Commendation.objects.create(teacher=lesson.teacher, subject=lesson.subject, created=lesson.date, schoolkid=schoolkid, text=praise)


def main():
    parser = argparse.ArgumentParser(description='Приветствую. ')
    parser.add_argument('--schoolkid', type=str, help='Введите имя ученика для улучшения оценок и добавления похвалы.')
    parser.add_argument('--subject', type=str, help='Введите название предмета по которому требуется добавить похввалу')
    args = parser.parse_args()
    try: 
        schoolkid = Schoolkid.objects.get(full_name__contains=args.schoolkid)
    except ObjectDoesNotExist:
        print("Такого ученика нет в базе!")
    except MultipleObjectsReturned:
        print("Найдено несколько учеников, уточните запрос!")
    fix_marks(schoolkid)
    del_chastisement(schoolkid)
    create_commendation(schoolkid, args.subject)


if __name__=="__main__": 
    main()