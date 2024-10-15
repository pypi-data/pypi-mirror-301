from haystack import Document
from haystack.components.classifiers import DocumentLanguageClassifier
from haystack.components.routers import MetadataRouter
from haystack.components.writers import DocumentWriter
from haystack.document_stores.in_memory import InMemoryDocumentStore

from ray_haystack.ray_pipeline import RayPipeline

documents = [
    Document(
        content="Super appartement. Juste au dessus de plusieurs bars qui ferment très tard. A savoir à l'avance. (Bouchons d'oreilles fournis !)"
    ),
    Document(
        content="El apartamento estaba genial y muy céntrico, todo a mano. Al lado de la librería Lello y De la Torre de los clérigos. Está situado en una zona de marcha, así que si vais en fin de semana , habrá ruido, aunque a nosotros no nos molestaba para dormir"
    ),
    Document(
        content="The keypad with a code is convenient and the location is convenient. Basically everything else, very noisy, wi-fi didn't work, check-in person didn't explain anything about facilities, shower head was broken, there's no cleaning and everything else one may need is charged."
    ),
    Document(
        content="It is very central and appartement has a nice appearance (even though a lot IKEA stuff), *W A R N I N G** the appartement presents itself as a elegant and as a place to relax, very wrong place to relax - you cannot sleep in this appartement, even the beds are vibrating from the bass of the clubs in the same building - you get ear plugs from the hotel -> now I understand why -> I missed a trip as it was so loud and I could not hear the alarm next day due to the ear plugs.- there is a green light indicating 'emergency exit' just above the bed, which shines very bright at night - during the arrival process, you felt the urge of the agent to leave as soon as possible. - try to go to 'RVA clerigos appartements' -> same price, super quiet, beautiful, city center and very nice staff (not an agency)- you are basically sleeping next to the fridge, which makes a lot of noise, when the compressor is running -> had to switch it off - but then had no cool food and drinks. - the bed was somehow broken down - the wooden part behind the bed was almost falling appart and some hooks were broken before- when the neighbour room is cooking you hear the fan very loud. I initially thought that I somehow activated the kitchen fan"
    ),
    Document(content="Un peu salé surtout le sol. Manque de service et de souplesse"),
    Document(
        content="Nous avons passé un séjour formidable. Merci aux personnes , le bonjours à Ricardo notre taxi man, très sympathique. Je pense refaire un séjour parmi vous, après le confinement, tout était parfait, surtout leur gentillesse, aucune chaude négative. Je n'ai rien à redire de négative, Ils étaient a notre écoute, un gentil message tout les matins, pour nous demander si nous avions besoins de renseignement et savoir si tout allait bien pendant notre séjour."
    ),
    Document(
        content="Céntrico. Muy cómodo para moverse y ver Oporto. Edificio con terraza propia en la última planta. Todo reformado y nuevo. Te traen un estupendo desayuno todas las mañanas al apartamento. Solo que se puede escuchar algo de ruido de la calle a primeras horas de la noche. Es un zona de ocio nocturno. Pero respetan los horarios."
    ),
]


def create_pipeline():
    en_document_store = InMemoryDocumentStore()
    fr_document_store = InMemoryDocumentStore()
    es_document_store = InMemoryDocumentStore()

    language_classifier = DocumentLanguageClassifier(languages=["en", "fr", "es"])
    router_rules = {
        "en": {"field": "meta.language", "operator": "==", "value": "en"},
        "fr": {"field": "meta.language", "operator": "==", "value": "fr"},
        "es": {"field": "meta.language", "operator": "==", "value": "es"},
    }
    router = MetadataRouter(rules=router_rules)

    en_writer = DocumentWriter(document_store=en_document_store)
    fr_writer = DocumentWriter(document_store=fr_document_store)
    es_writer = DocumentWriter(document_store=es_document_store)

    indexing_pipeline = RayPipeline()
    indexing_pipeline.add_component(instance=language_classifier, name="language_classifier")
    indexing_pipeline.add_component(instance=router, name="router")
    indexing_pipeline.add_component(instance=en_writer, name="en_writer")
    indexing_pipeline.add_component(instance=fr_writer, name="fr_writer")
    indexing_pipeline.add_component(instance=es_writer, name="es_writer")

    indexing_pipeline.connect("language_classifier", "router")
    indexing_pipeline.connect("router.en", "en_writer")
    indexing_pipeline.connect("router.fr", "fr_writer")
    indexing_pipeline.connect("router.es", "es_writer")

    return indexing_pipeline
