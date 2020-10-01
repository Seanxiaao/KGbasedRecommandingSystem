# Project Proposal

### Project Name 

Knowledge Graph-Enhanced Musical Hooks Recommender System

### Project Members:

Ian Myoungsu Choi / Ye Xiao

### Project Domains and Goals

Musical hooks can be thought of as catchy fragments of the original music, which are easily recalled to users’ minds and lead them to want to repeat to listen. For this reason, politicians commonly use linguistic hooks (catchphrases) as their rhetoric strategy. Musical hooks are obviously one of the most important factors that users select a certain song. In this work, we aim to build a system that can recommend musical hooks itself based on the following information: 1) latent representations of the hooks, 2) the music metadata related to the hooks (e.g. rhymes, repetitive part of the lyrics, genre, instrument, artist, etc), and 3) interaction between users and music. In order to incorporate external information such as the abovementioned 2) and 3), we introduce knowledge graphs into the system. In doing so, the performance of the system is expected to be augmented and the recommendations of the system can be explainable to the users. 

### Stretch Goals [Beyond the scope of the class project]

Ideally, we would like to provide users with:
Similar hooks based on each perspective (melodic/rhythmical/lyrical).
The modified version of the similar hooks.
The re-mixed version that is smoothly connected with the several hooks.

### Datasets [This can be changed.]

MusicBrainz: https://musicbrainz.org/
Last.fm: https://www.last.fm/
AllMusic: https://www.allmusic.com/

### Technical Challenge

- [ ] Extracting rhymes and repetitive parts of the lyrics from the song.

- [ ] Determining how to build a knowledge graph that consists of IDs, titles, rhymes, and repetitive parts of the lyrics.

- [ ] Extracting the latent representations of the hooks of the songs.

- [ ] Determining how to utilize the knowledge graphs for improving the recommendations generated from the embeddings of the hooks.

  For the purpose of the project, this task will be simplified in a way that:

  1. First, all the songs will be padded so that they can have the same length.
  2. Each song will be divided into k fragments.
  3. The embeddings are supposed to be extracted based on the fragments. When a user specifies the start/end point of the hooks in a certain song, the most overlapped fragment from the above step will be considered as the user’s selection.

