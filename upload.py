import glob
import os

from google.cloud import storage


def upload():
    cred_file = 'data/YAWN-service-account.json'
    if os.path.exists(cred_file):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_file

    public_url = os.environ['PUBLIC_URL'].strip('/')
    client = storage.Client()
    bucket = client.bucket('static.yawn.live')

    existing = bucket.list_blobs(prefix=public_url)
    bucket.delete_blobs(existing)

    for filename in glob.glob('build/**', recursive=True):
        if os.path.isdir(filename):
            continue
        path = f'{public_url}/{filename.replace("build/", "")}'
        print(f'Uploading {path}')
        blob = bucket.blob(path)
        blob.upload_from_filename(filename)
        blob.make_public()

    print('')
    print(f'View the site at http://static.yawn.live/{public_url}/')
    print('')


if __name__ == '__main__':
    upload()
