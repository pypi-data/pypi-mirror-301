import os
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Set

import torch
from safetensors.torch import load_file, save_file

# def _remove_duplicate_names(
#     state_dict: Dict[str, torch.Tensor],
#     *,
#     preferred_names: List[str] = None,
#     discard_names: List[str] = None,
# ) -> Dict[str, List[str]]:
#     if preferred_names is None:
#         preferred_names = []
#     preferred_names = set(preferred_names)
#     if discard_names is None:
#         discard_names = []
#     discard_names = set(discard_names)

#     shareds = _find_shared_tensors(state_dict)
#     to_remove = defaultdict(list)
#     for shared in shareds:
#         complete_names = set(
#             [name for name in shared if _is_complete(state_dict[name])]
#         )
#         if not complete_names:
#             if len(shared) == 1:
#                 # Force contiguous
#                 name = list(shared)[0]
#                 state_dict[name] = state_dict[name].clone()
#                 complete_names = {name}
#             else:
#                 raise RuntimeError(
#                     f"Error while trying to find names to remove to save state dict, but found no suitable name to keep for saving amongst: {shared}. None is covering the entire storage.Refusing to save/load the model since you could be storing much more memory than needed. Please refer to https://huggingface.co/docs/safetensors/torch_shared_tensors for more information. Or open an issue."
#                 )

#         keep_name = sorted(list(complete_names))[0]

#         # Mecanism to preferentially select keys to keep
#         # coming from the on-disk file to allow
#         # loading models saved with a different choice
#         # of keep_name
#         preferred = complete_names.difference(discard_names)
#         if preferred:
#             keep_name = sorted(list(preferred))[0]

#         if preferred_names:
#             preferred = preferred_names.intersection(complete_names)
#             if preferred:
#                 keep_name = sorted(list(preferred))[0]
#         for name in sorted(shared):
#             if name != keep_name:
#                 to_remove[keep_name].append(name)
#     return to_remove


# def get_discard_names(
#     model_id: str, revision: Optional[str], folder: str, token: Optional[str]
# ) -> List[str]:
#     try:
#         import json

#         import transformers

#         # config_filename = hf_hub_download(
#         #     model_id,
#         #     revision=revision,
#         #     filename="config.json",
#         #     token=token,
#         #     cache_dir=folder,
#         # )
#         with open(config_filename, "r") as f:
#             config = json.load(f)
#         architecture = config["architectures"][0]

#         class_ = getattr(transformers, architecture)

#         # Name for this varible depends on transformers version.
#         discard_names = getattr(class_, "_tied_weights_keys", [])

#     except Exception:
#         discard_names = []
#     return discard_names


class AlreadyExists(Exception):
    pass


def check_file_size(sf_filename: str, pt_filename: str):
    sf_size = os.stat(sf_filename).st_size
    pt_size = os.stat(pt_filename).st_size

    if (sf_size - pt_size) / pt_size > 0.01:
        raise RuntimeError(
            f"""The file size different is more than 1%:
         - {sf_filename}: {sf_size}
         - {pt_filename}: {pt_size}
         """
        )


def rename(pt_filename: str) -> str:
    filename, ext = os.path.splitext(pt_filename)
    local = f"{filename}.safetensors"
    local = local.replace("pytorch_model", "model")
    return local


# def convert_multi(
#     model_id: str,
#     *,
#     revision=Optional[str],
#     folder: str,
#     token: Optional[str],
#     discard_names: List[str],
# ) -> ConversionResult:
#     filename = hf_hub_download(
#         repo_id=model_id,
#         revision=revision,
#         filename="pytorch_model.bin.index.json",
#         token=token,
#         cache_dir=folder,
#     )
#     with open(filename, "r") as f:
#         data = json.load(f)

#     filenames = set(data["weight_map"].values())
#     local_filenames = []
#     for filename in filenames:
#         pt_filename = hf_hub_download(
#             repo_id=model_id, filename=filename, token=token, cache_dir=folder
#         )

#         sf_filename = rename(pt_filename)
#         sf_filename = os.path.join(folder, sf_filename)
#         convert_file(pt_filename, sf_filename, discard_names=discard_names)
#         local_filenames.append(sf_filename)

#     index = os.path.join(folder, "model.safetensors.index.json")
#     with open(index, "w") as f:
#         newdata = {k: v for k, v in data.items()}
#         newmap = {k: rename(v) for k, v in data["weight_map"].items()}
#         newdata["weight_map"] = newmap
#         json.dump(newdata, f, indent=4)
#     local_filenames.append(index)

#     operations = [
#         CommitOperationAdd(path_in_repo=os.path.basename(local), path_or_fileobj=local)
#         for local in local_filenames
#     ]
#     errors: List[Tuple[str, "Exception"]] = []

#     return operations, errors


def convert_single(pt_filename: Path) -> None:
    sf_name = "converted_model.safetensors"
    sf_filename = pt_filename.parent / sf_name
    convert_file(pt_filename, sf_filename)


def convert_file(
    pt_filename: Path,
    sf_filename: Path,
) -> None:
    loaded = torch.load(pt_filename, map_location="cpu")
    if "state_dict" in loaded:
        loaded = loaded["state_dict"]

    metadata = {"format": "pt"}

    # Force tensors to be contiguous
    loaded = {k: v.contiguous() for k, v in loaded.items()}

    # dirname = os.path.dirname(sf_filename)
    # os.makedirs(dirname, exist_ok=True)
    save_file(loaded, sf_filename, metadata=metadata)
    check_file_size(sf_filename, pt_filename)
    reloaded = load_file(sf_filename)
    for k in loaded:
        pt_tensor = loaded[k]
        sf_tensor = reloaded[k]
        if not torch.equal(pt_tensor, sf_tensor):
            raise RuntimeError(f"The output tensors do not match for key {k}")


def convert_generic(
    pt_filename: str,
    *,
    folder: str,
    filenames: Set[str],
) -> None:
    errors = []

    extensions = set([".bin", ".ckpt"])
    for filename in filenames:
        prefix, ext = os.path.splitext(filename)
        if ext in extensions:
            dirname, raw_filename = os.path.split(filename)
            if raw_filename == "pytorch_model.bin":
                # XXX: This is a special case to handle `transformers` and the
                # `transformers` part of the model which is actually loaded by `transformers`.
                sf_in_repo = os.path.join(dirname, "model.safetensors")
            else:
                sf_in_repo = f"{prefix}.safetensors"
            sf_filename = os.path.join(folder, sf_in_repo)
            try:
                convert_file(pt_filename, sf_filename)
            except Exception as e:
                errors.append((pt_filename, e))


def convert(pt_file: Path, force: bool = False) -> None:
    with TemporaryDirectory() as _:
        folder = pt_file.parent / "forge_tmp"
        folder.mkdir(exist_ok=True)
        try:
            if pt_file.suffix == ".safetenors" and not force:
                raise AlreadyExists(
                    f"Model {pt_file.stem} is already converted, skipping.."
                )
            # elif library_name == "transformers":
            #     discard_names = get_discard_names(
            #         model_id, revision=revision, folder=folder, token=api.token
            #     )
            #     if "pytorch_model.bin" in filenames:
            convert_single(pt_file)
            #     elif "pytorch_model.bin.index.json" in filenames:
            #         operations, errors = convert_multi(
            #             model_id,
            #             revision=revision,
            #             folder=folder,
            #             token=api.token,
            #             discard_names=discard_names,
            #         )
            #     else:
            #         raise RuntimeError(
            #             f"Model {model_id} doesn't seem to be a valid pytorch model. Cannot convert"
            #         )
            # else:
            #     operations, errors = convert_generic(
            #         model_id,
            #         revision=revision,
            #         folder=folder,
            #         filenames=filenames,
            #         token=api.token,
            #     )

            # if operations:
            #     new_pr = api.create_commit(
            #         repo_id=model_id,
            #         revision=revision,
            #         operations=operations,
            #         commit_message=pr_title,
            #         commit_description=COMMIT_DESCRIPTION,
            #         create_pr=True,
            #     )
            #     print(f"Pr created at {new_pr.pr_url}")
            # else:
            #     print("No files to convert")
        finally:
            shutil.rmtree(folder)
