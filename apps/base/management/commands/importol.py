from django.core.management.base import BaseCommand, CommandError
from base.models import Genre, Book, Author, Publisher
import csv
import json
import sys

class Command(BaseCommand):
    help = 'Imports Books and Authors from an openlibrary dump file'

    def add_arguments(self, parser):
        parser.add_argument('ol_dump', help='The location of the OpenLibrary dump file', type=str)
        parser.add_argument('-p', '--default-publisher', help="PK of the default Publisher", default=1, type=int)
        parser.add_argument('-a', '--default-author', help='PK of the default Author', default=1, type=int)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Loading from: {}".format(options['ol_dump'])))
        default_author = Author.objects.get(pk=options['default_author'])
        default_publisher = Publisher.objects.get(pk=options['default_publisher'])
        count = 0
        with open(options['ol_dump']) as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                count += 1
                record = json.loads(row[4])
                if row[0] == "/type/author":
                    author = Author(name=record['name'],
                        ol_id=row[1].split("/")[-1])
                    if 'personal_name' in record:
                        author.alternate_names = record['personal_name']
                    if "alternate_names" in record:
                        author.alternate_names += ",".join(record['alternate_names'])[:1023]
                    if 'birth_date' in record:
                        author.year_of_birth = record['birth_date']
                    if 'death_date' in record:
                        author.year_of_death = record['death_date']
                    try:
                        author.save()
                    except:
                        pass
                elif row[0] == "/type/edition":
                    try:
                        book = Book(title=record['title'],
                            ol_id=row[1].split("/")[-1])
                    except KeyError:
                        print("No title for: {}".format(row[1].split("/")[-1]))
                        continue
                    if 'publish_date' in record:
                        book.year_of_publication = record['publish_date']
                    if 'publishers' in record:
                        publisher, created = Publisher.objects.get_or_create(
                                name=record['publishers'][0][:254]
                                )
                        book.publisher = publisher
                    else:
                        book.publisher = default_publisher
                    if 'identifiers' in record:
                        if 'isbn_13' in record['identifiers']:
                            book.isbn = record['identifiers']['isbn_13'][0]
                        elif 'isbn_10' in record['identifiers']:
                            book.isbn = record['identifiers']['isbn_10'][0]
                    if 'authors' in record:
                        try:
                            book.save()
                            for author in record['authors']:
                                try:
                                    book.authors.add(
                                        Author.objects.get(ol_id=author['key'].split("/")[-1])
                                        )
                                except Author.DoesNotExist:
                                    book.authors.add(default_author)
                        except:
                            pass
                    try:
                        book.save()
                    except:
                        pass

                elif row[0] == "/type/work":
                    try:
                        work = Work(title=record['title'],
                                ol_id=row[1].split("/")[-1])
                    except KeyError:
                        print("No title for: {}".format(row[1].split("/")[-1]))
                        continue

                    if 'authors' in record:
                        try:
                            work.save()
                        for author in record['authors']:
                            try:
                                work.authors.add(
                                    Auhtor.objects.get(ol_id=author['author']['key'].split("/")[-1])
                                )
                            except: Author.DoesNotExist:
                                work.authors.add(default_author)

                    try:
                        work.save()
                    except:
                        pass

                if count % 100 == 0:
                    self.stdout.write(self.style.WARNING("Completed {} rows".format(count)))
